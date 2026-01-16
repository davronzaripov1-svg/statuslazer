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

# New formula - distributes orders sequentially based on queue position
# Logic:
# 1. Calculate total sheets in orders BEFORE this one (by date, not finished)
# 2. Based on running total, assign to A or B in alternating blocks of 400
new_formula = '=IF(OR(E2="";H2="");"";LET(before;SUMIFS($E$2:$E;$F$2:$F;"<>Готов";$B$2:$B;"<"&B2)+SUMIFS($E$2:E2;$F$2:F2;"<>Готов";$B$2:B2;B2;ROW($A$2:A2);"<"&ROW(A2));total;before+E2;IF(total<=400;"A";IF(total<=800;IF(H2="Доставка";IF(total<=600;"B";"A");"B");IF(total<=1400;"A";IF(total<=2000;IF(H2="Доставка";IF(total<=1600;"B";"⛔ Стоп");"B");"⛔ Стоп"))))))'

# Update cell I2
sheet.update_acell('I2', new_formula)
print('Формула обновлена в I2')

# Copy formula down - need to adjust row references
updates = []
for row in range(3, 501):
    formula = new_formula.replace('E2', f'E{row}').replace('H2', f'H{row}').replace('B2', f'B{row}').replace('F2', f'F{row}').replace('A2', f'A{row}').replace(f'ROW(A{row})', f'ROW(A{row})')
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
