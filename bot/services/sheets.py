import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from bot.config import SPREADSHEET_ID, SHEET_NAME, Columns


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


@dataclass
class CapacityCheckResult:
    can_accept: bool
    recommended_machine: str
    ready_date: str
    row_number: int


@dataclass
class OrderInfo:
    order_number: int
    status: str
    sheets_count: int
    machine: str
    ready_date: str
    row_number: int


class SheetsService:
    def __init__(self, credentials_file: str = "credentials.json"):
        creds = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
        self.sheet = self.spreadsheet.worksheet(SHEET_NAME)

    def _get_next_order_number(self) -> int:
        """Get next order number based on existing data"""
        all_values = self.sheet.col_values(Columns.ORDER_NUMBER + 1)
        # Skip header, find max number
        numbers = []
        for val in all_values[1:]:
            try:
                # Handle "#0003" format
                clean_val = val.replace('#', '').strip()
                numbers.append(int(clean_val))
            except (ValueError, TypeError):
                continue
        return max(numbers, default=0) + 1

    def _find_first_empty_row(self) -> int:
        """Find first row where column A (order number) is empty"""
        order_numbers = self.sheet.col_values(Columns.ORDER_NUMBER + 1)
        for i, val in enumerate(order_numbers[1:], start=2):  # Skip header, rows start at 2
            if not val or val.strip() == '':
                return i
        # If no empty row found, return next row after last
        return len(order_numbers) + 1

    def create_draft_order(
        self,
        client_type: str,
        delivery: str,
        sheets_count: int,
        telegram_id: int,
        username: str,
        chat_id: int
    ) -> CapacityCheckResult:
        """
        Create a draft row to check capacity.
        Returns capacity check result with can_accept, machine, date.
        """
        order_number = self._get_next_order_number()
        now_full = datetime.now().strftime("%d.%m.%Y %H:%M")

        # Find first empty row (with formulas already in place)
        row_number = self._find_first_empty_row()

        # Update cells in the empty row (only data columns, not formula columns)
        updates = [
            (row_number, Columns.ORDER_NUMBER + 1, order_number),
            (row_number, Columns.ACCEPTANCE_DATE + 1, now_full),  # Full datetime for time-based calculations
            (row_number, Columns.CLIENT_TYPE + 1, client_type),
            (row_number, Columns.SHEETS_COUNT + 1, sheets_count),
            (row_number, Columns.STATUS + 1, "Черновик"),
            (row_number, Columns.DELIVERY + 1, delivery),
            (row_number, Columns.TELEGRAM_ID + 1, telegram_id),
            (row_number, Columns.TELEGRAM_USERNAME + 1, username or ""),
            (row_number, Columns.CHAT_ID + 1, chat_id),
            (row_number, Columns.SOURCE + 1, "Бот"),
            (row_number, Columns.CREATED_BY + 1, "Бот"),
            (row_number, Columns.CREATED_DATE + 1, now_full),
        ]

        # Batch update for efficiency
        for r, c, val in updates:
            self.sheet.update_cell(r, c, val)

        # Wait for formula I (recommended machine) to calculate
        import time
        time.sleep(2)

        # Read recommended machine from formula column I
        recommended_machine = self.sheet.cell(row_number, Columns.RECOMMENDED_MACHINE + 1).value or "A"

        # Set actual machine (G) to recommended machine so formulas J, K, L work correctly
        self.sheet.update_cell(row_number, Columns.MACHINE + 1, recommended_machine)

        # Wait for other formulas to recalculate
        time.sleep(2)

        # Force fresh read using get() with specific range (bypasses cache)
        range_name = f"A{row_number}:U{row_number}"
        result = self.sheet.get(range_name, value_render_option='FORMATTED_VALUE')
        row_data = result[0] if result else []

        # Extend row_data if shorter than expected
        while len(row_data) < 21:
            row_data.append('')

        can_accept_val = row_data[Columns.CAN_ACCEPT].upper().strip()
        can_accept = can_accept_val in ('ДА', 'YES', 'TRUE', '1')

        return CapacityCheckResult(
            can_accept=can_accept,
            recommended_machine=row_data[Columns.RECOMMENDED_MACHINE] or "—",
            ready_date=row_data[Columns.READY_DATE] or "—",
            row_number=row_number
        )

    def confirm_order(self, row_number: int, file_url: str, machine: str) -> int:
        """
        Confirm draft order: set status, file URL, and fix machine.
        Returns order number.
        """
        # Update status
        self.sheet.update_cell(row_number, Columns.STATUS + 1, "В очереди")
        # Update file URL
        self.sheet.update_cell(row_number, Columns.FILE_URL + 1, file_url)
        # Fix machine (copy from recommended to actual)
        self.sheet.update_cell(row_number, Columns.MACHINE + 1, machine)
        # Update acceptance date with full time
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.sheet.update_cell(row_number, Columns.ACCEPTANCE_DATE + 1, now)

        # Get order number
        order_number = self.sheet.cell(row_number, Columns.ORDER_NUMBER + 1).value
        return int(order_number)

    def delete_draft(self, row_number: int):
        """Clear draft row data if order was rejected (keeps formulas)"""
        # Clear only data columns, not formula columns (I, J, K, L, M, U)
        data_columns = [
            Columns.ORDER_NUMBER,      # A
            Columns.ACCEPTANCE_DATE,   # B
            Columns.CLIENT,            # C
            Columns.CLIENT_TYPE,       # D
            Columns.SHEETS_COUNT,      # E
            Columns.STATUS,            # F
            Columns.MACHINE,           # G
            Columns.DELIVERY,          # H
            Columns.TELEGRAM_ID,       # N
            Columns.TELEGRAM_USERNAME, # O
            Columns.CHAT_ID,           # P
            Columns.FILE_URL,          # Q
            Columns.SOURCE,            # R
            Columns.CREATED_BY,        # S
            Columns.CREATED_DATE,      # T
        ]
        for col in data_columns:
            self.sheet.update_cell(row_number, col + 1, "")

    def update_order_status(self, order_number: int, new_status: str) -> bool:
        """Update order status by order number"""
        all_data = self.sheet.get_all_values()

        for i, row in enumerate(all_data[1:], start=2):
            if len(row) < 1:
                continue
            # Handle both "6" and "#0006" formats
            row_order = str(row[Columns.ORDER_NUMBER]).replace('#', '').strip()
            try:
                if int(row_order) == order_number:
                    self.sheet.update_cell(i, Columns.STATUS + 1, new_status)
                    return True
            except ValueError:
                continue

        return False

    def get_user_orders(self, telegram_id: int, limit: int = 10) -> list[OrderInfo]:
        """Get user's orders by Telegram ID"""
        all_data = self.sheet.get_all_values()
        orders = []

        for i, row in enumerate(all_data[1:], start=2):  # Skip header, rows start at 2
            if len(row) < 21:
                row.extend([''] * (21 - len(row)))

            try:
                row_telegram_id = int(row[Columns.TELEGRAM_ID]) if row[Columns.TELEGRAM_ID] else 0
            except ValueError:
                continue

            if row_telegram_id == telegram_id and row[Columns.STATUS] != "Черновик":
                try:
                    order_number = int(row[Columns.ORDER_NUMBER]) if row[Columns.ORDER_NUMBER] else 0
                except ValueError:
                    order_number = 0

                try:
                    sheets_count = int(row[Columns.SHEETS_COUNT]) if row[Columns.SHEETS_COUNT] else 0
                except ValueError:
                    sheets_count = 0

                orders.append(OrderInfo(
                    order_number=order_number,
                    status=row[Columns.STATUS] or "—",
                    sheets_count=sheets_count,
                    machine=row[Columns.MACHINE] or "—",
                    ready_date=row[Columns.READY_DATE] or "—",
                    row_number=i
                ))

        # Return last N orders (most recent first)
        return sorted(orders, key=lambda x: x.order_number, reverse=True)[:limit]

    def get_order_by_number(self, order_number: int, telegram_id: int) -> Optional[OrderInfo]:
        """Get specific order by number (only if belongs to user)"""
        all_data = self.sheet.get_all_values()

        for i, row in enumerate(all_data[1:], start=2):
            if len(row) < 21:
                row.extend([''] * (21 - len(row)))

            try:
                row_order_num = int(row[Columns.ORDER_NUMBER]) if row[Columns.ORDER_NUMBER] else 0
                row_telegram_id = int(row[Columns.TELEGRAM_ID]) if row[Columns.TELEGRAM_ID] else 0
            except ValueError:
                continue

            if row_order_num == order_number and row_telegram_id == telegram_id:
                try:
                    sheets_count = int(row[Columns.SHEETS_COUNT]) if row[Columns.SHEETS_COUNT] else 0
                except ValueError:
                    sheets_count = 0

                return OrderInfo(
                    order_number=order_number,
                    status=row[Columns.STATUS] or "—",
                    sheets_count=sheets_count,
                    machine=row[Columns.MACHINE] or "—",
                    ready_date=row[Columns.READY_DATE] or "—",
                    row_number=i
                )

        return None

    def hide_order_from_user(self, order_number: int, telegram_id: int) -> bool:
        """Hide order from user's list by clearing telegram_id"""
        all_data = self.sheet.get_all_values()

        for i, row in enumerate(all_data[1:], start=2):
            if len(row) < 21:
                row.extend([''] * (21 - len(row)))

            try:
                row_order_num = int(row[Columns.ORDER_NUMBER]) if row[Columns.ORDER_NUMBER] else 0
                row_telegram_id = int(row[Columns.TELEGRAM_ID]) if row[Columns.TELEGRAM_ID] else 0
            except ValueError:
                continue

            if row_order_num == order_number and row_telegram_id == telegram_id:
                # Clear telegram_id to hide from user's view
                self.sheet.update_cell(i, Columns.TELEGRAM_ID + 1, "")
                return True

        return False


# Singleton instance
_sheets_service: Optional[SheetsService] = None


def get_sheets_service() -> SheetsService:
    global _sheets_service
    if _sheets_service is None:
        _sheets_service = SheetsService()
    return _sheets_service
