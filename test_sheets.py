# -*- coding: utf-8 -*-
import gspread
from google.oauth2.service_account import Credentials
import sys
sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = "1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo"

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet("ЗАКАЗЫ")

# Check last orders
all_data = sheet.get_all_values()
print("Recent orders with formula values:\n")

for i, row in enumerate(all_data[1:6], start=2):  # First 5 data rows
    while len(row) < 21:
        row.append('')
    if row[0]:  # Has order number
        print(f"Row {i} - Order {row[0]}:")
        print(f"  B (Дата принятия): {row[1]}")
        print(f"  E (Листов): {row[4]}")
        print(f"  J (Листов впереди): {row[9]}")
        print(f"  K (Дней производства): {row[10]}")
        print(f"  L (Дата готовности): {row[11]}")
        print()
