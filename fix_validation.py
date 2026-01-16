import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sh = gc.open_by_key("1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo")
sheet = sh.worksheet("ЗАКАЗЫ")

# Get current data validation for column F (Status)
# We need to update the validation to include all statuses:
# Черновик, В очереди, В работе, Готов, Отклонён, Отправлен

# Use the Sheets API directly to set data validation
spreadsheet_id = "1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo"

# All valid statuses
statuses = ["Черновик", "В очереди", "В работе", "Готов", "Отклонён", "Отправлен"]

# Create data validation request
request = {
    "requests": [
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet.id,
                    "startRowIndex": 1,  # Skip header row
                    "endRowIndex": 1000,
                    "startColumnIndex": 5,  # Column F (0-indexed)
                    "endColumnIndex": 6
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [{"userEnteredValue": s} for s in statuses]
                    },
                    "inputMessage": "Выберите статус",
                    "strict": True,
                    "showCustomUi": True
                }
            }
        }
    ]
}

# Execute the request
sh.batch_update(request)
print("Валидация обновлена!")
print(f"Доступные статусы: {', '.join(statuses)}")
