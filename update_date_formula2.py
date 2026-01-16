import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sh = gc.open_by_key("1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo")
sheet = sh.worksheet("ЗАКАЗЫ")

# More precise formula for column L (Дата готовности)
# Logic:
# 1. remaining_hours = 20 - HOUR(B2) (hours left today until 20:00)
# 2. sheets_can_do_today = remaining_hours * 20 (sheets per hour)
# 3. If this_order_sheets > sheets_can_do_today, add 1 extra day
# 4. Add K2-1 days for queue ahead
# 5. Use WORKDAY to skip weekends

# Formula:
# LET(
#   remaining_hours, MAX(0, 20 - HOUR(B2)),
#   can_today, remaining_hours * 20,
#   extra, IF(E2 > can_today, 1, 0),
#   WORKDAY.INTL(INT(B2), MAX(K2-1, 0) + extra, 'НАСТРОЙКИ'!E2)
# )

new_formula = '=IF(OR(E2="";B2="");"";LET(rem_hrs;MAX(0;20-HOUR(B2));can_today;rem_hrs*20;extra;IF(E2>can_today;1;0);WORKDAY.INTL(INT(B2);MAX(K2-1;0)+extra;\'НАСТРОЙКИ\'!E2)))'

# Update L2
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

print()
print('Готово! Новая логика:')
print('- Оставшееся время = 20:00 - время заказа')
print('- Можем сегодня = оставшиеся часы × 20 листов/час')
print('- Если листов > можем сегодня → +1 день')
print()
print('Пример: заказ в 18:00 на 80 листов')
print('- Осталось 2 часа = 40 листов макс')
print('- 80 > 40 → готовность на следующий день')
