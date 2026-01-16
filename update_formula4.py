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

# For row 2 (first order): A_load=0, B_load=0, so always recommend A if sheets <= 400
formula_row2 = '=IF(OR(E2="";H2="");"";IF(E2<=400;"A";IF(E2<=800;"B";"⛔ Стоп")))'
sheet.update_acell('I2', formula_row2)
print('Формула обновлена в I2')

# For rows 3+: use SUMPRODUCT to look at rows above
updates = []
for row in range(3, 501):
    prev_row = row - 1
    formula = f'=IF(OR(E{row}="";H{row}="");"";LET(A_load;SUMPRODUCT(($G$2:G{prev_row}="A")*($F$2:F{prev_row}<>"Готов")*($E$2:E{prev_row}));B_load;SUMPRODUCT(($G$2:G{prev_row}="B")*($F$2:F{prev_row}<>"Готов")*($E$2:E{prev_row}));IF(A_load+E{row}<=400;"A";IF(B_load+E{row}<=400;"B";IF(A_load+E{row}<=1000;"A";IF(B_load+E{row}<=1000;"B";"⛔ Стоп"))))))'
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
