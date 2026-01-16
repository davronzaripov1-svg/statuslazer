import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sh = gc.open_by_key("1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo")
sheet = sh.worksheet("ЗАКАЗЫ")

# New formula for column L (Дата готовности)
# Logic:
# 1. Calculate remaining hours today = end_time(20:00) - order_time
# 2. Calculate sheets that can be done today = remaining_hours * sheets_per_hour
# 3. Calculate remaining sheets for future days
# 4. Calculate additional days needed
# 5. Return the ready date

# Simpler approach for now:
# - Calculate total hours needed = (sheets_ahead + this_sheets) / sheets_per_hour
# - Calculate days = ceiling(hours / hours_per_day)
# - If order placed after 18:00, add 1 day
# - Use WORKDAY to skip weekends

# Formula explanation:
# K2 = days of production (based on sheets ahead)
# B2 = acceptance datetime
# If HOUR(B2) >= 18, add 1 extra day (order came late)
# Minimum 1 day for any order

new_formula = '=IF(OR(E2="";B2="");"";WORKDAY.INTL(INT(B2);MAX(K2-1;0)+IF(HOUR(B2)>=18;1;0);\'НАСТРОЙКИ\'!E2))'

# Update I2 first
sheet.update_acell('L2', new_formula)
print('Формула L2 обновлена')

# Copy to remaining rows
updates = []
for row in range(3, 501):
    formula = new_formula.replace('E2', f'E{row}').replace('B2', f'B{row}').replace('K2', f'K{row}')
    updates.append({
        'range': f'L{row}',
        'values': [[formula]]
    })

for i in range(0, len(updates), 100):
    chunk = updates[i:i+100]
    sheet.batch_update(chunk, value_input_option='USER_ENTERED')
    print(f'Обновлено строк: {min(i+100, len(updates))}')

print('Готово! Теперь заказы после 18:00 автоматически +1 день')
