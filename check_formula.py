import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sh = gc.open_by_key("1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo")
sheet = sh.worksheet("ЗАКАЗЫ")

print("=== Текущие заказы ===")
print("Строка | Листов | G    | I    | Статус     | A_до  | B_до")
print("-" * 60)

data = sheet.get("A2:I15")
a_total = 0
b_total = 0
for i, row in enumerate(data, start=2):
    if len(row) >= 5 and row[0]:
        sheets = int(row[4]) if row[4] else 0
        status = row[5] if len(row) > 5 else ""
        machine_g = row[6] if len(row) > 6 else ""
        machine_i = row[8] if len(row) > 8 else ""

        print(f"{i:6} | {sheets:6} | {machine_g:4} | {machine_i:4} | {status:10} | {a_total:5} | {b_total:5}")

        # Accumulate for next row (only if not finished)
        if "Готов" not in status:
            if machine_g == "A":
                a_total += sheets
            elif machine_g == "B":
                b_total += sheets
