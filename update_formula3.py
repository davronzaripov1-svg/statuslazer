import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import gspread
from google.oauth2.service_account import Credentials

scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
gc = gspread.authorize(creds)

spreadsheet_id = '1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo'
sh = gc.open_by_key(spreadsheet_id)
sheet = sh.worksheet('ЗАКАЗЫ')

# New formula - looks at actual assignments (G column) of orders BEFORE this one
# Logic:
# 1. A_load = sum of sheets assigned to A (column G) for orders before this one (by date)
# 2. B_load = sum of sheets assigned to B for orders before this one
# 3. If A_load + this order <= 400 → A
# 4. Else if B_load + this order <= 400 → B
# 5. Else if A_load + this order <= 1000 → A
# 6. Else if B_load + this order <= 1000 → B
# 7. Else → Stop

new_formula = '=IF(OR(E2="";H2="");"";LET(A_load;SUMIFS($E$2:$E$500;$G$2:$G$500;"A";$F$2:$F$500;"<>Готов";$B$2:$B$500;"<"&B2);B_load;SUMIFS($E$2:$E$500;$G$2:$G$500;"B";$F$2:$F$500;"<>Готов";$B$2:$B$500;"<"&B2);IF(A_load+E2<=400;"A";IF(B_load+E2<=400;"B";IF(A_load+E2<=1000;"A";IF(B_load+E2<=1000;"B";"⛔ Стоп"))))))'

# Update cell I2
sheet.update_acell('I2', new_formula)
print('Формула обновлена в I2')

# Copy formula down - adjust row references for E2, H2, B2
updates = []
for row in range(3, 501):
    formula = new_formula.replace('E2', f'E{row}').replace('H2', f'H{row}').replace('B2', f'B{row}')
    updates.append({
        'range': f'I{row}',
        'values': [[formula]]
    })

# Batch update
for i in range(0, len(updates), 100):
    chunk = updates[i:i+100]
    sheet.batch_update(chunk, value_input_option='USER_ENTERED')
    print(f'Обновлено строк: {min(i+100, len(updates))}')

print('Готово!')
