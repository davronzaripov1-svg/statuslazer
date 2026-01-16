import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sh = gc.open_by_key("1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo")
sheet = sh.worksheet("ЗАКАЗЫ")

# Problem: Current formula doesn't account for THIS order's sheets in date calculation
#
# Current logic:
#   K = days for sheets AHEAD (J / 200)
#   L = date based on K
#   But 2999 sheets in current order = ~15 days, not counted!
#
# New logic:
#   Total sheets to complete = sheets_ahead (J) + this_order (E)
#   Total days = CEILING((J + E) / sheets_per_day)
#   Consider remaining hours today

# New formula for K (Дней на изготовление):
# Include BOTH sheets ahead AND current order sheets
k_formula = '=IF(OR(E2="";G2="");"";CEILING((J2+E2)/\'НАСТРОЙКИ\'!$A$2;1))'

print("Обновляю формулу K (дней на изготовление)...")
sheet.update_acell('K2', k_formula)

# Copy to remaining rows
updates = []
for row in range(3, 501):
    formula = k_formula.replace('E2', f'E{row}').replace('J2', f'J{row}').replace('G2', f'G{row}')
    updates.append({
        'range': f'K{row}',
        'values': [[formula]]
    })

for i in range(0, len(updates), 100):
    chunk = updates[i:i+100]
    sheet.batch_update(chunk, value_input_option='USER_ENTERED')
    print(f'K обновлено: {min(i+100, len(updates))} строк')

# Update L formula (ready date) - simpler now since K already has total days
# L = WORKDAY from order date + (K-1) days (since day 1 is order day)
l_formula = '=IF(OR(E2="";B2="";K2="");"";WORKDAY.INTL(INT(B2);K2-1;\'НАСТРОЙКИ\'!$E$2))'

print()
print("Обновляю формулу L (дата готовности)...")
sheet.update_acell('L2', l_formula)

updates = []
for row in range(3, 501):
    formula = l_formula.replace('E2', f'E{row}').replace('B2', f'B{row}').replace('K2', f'K{row}')
    updates.append({
        'range': f'L{row}',
        'values': [[formula]]
    })

for i in range(0, len(updates), 100):
    chunk = updates[i:i+100]
    sheet.batch_update(chunk, value_input_option='USER_ENTERED')
    print(f'L обновлено: {min(i+100, len(updates))} строк')

print()
print("Готово!")
print()
print("Новая логика:")
print("- K = CEILING((листов_впереди + листов_заказа) / 200)")
print("- L = рабочий день через K-1 дней от даты заказа")
print()
print("Пример: 2999 листов, очередь пустая")
print(f"- K = CEILING((0 + 2999) / 200) = CEILING(14.995) = 15 дней")
print("- L = дата заказа + 14 рабочих дней")
