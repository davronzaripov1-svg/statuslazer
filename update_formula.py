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

# New formula for column I (row 2)
new_formula = '=IF(OR(E2="";H2="");"";IF(\'КОНТРОЛЬ МОЩНОСТИ\'!A1+E2<=400;"A";IF(H2="Самовывоз";IF(\'КОНТРОЛЬ МОЩНОСТИ\'!B1+E2<=400;"B";IF(\'КОНТРОЛЬ МОЩНОСТИ\'!A1+E2<=1000;"A";IF(\'КОНТРОЛЬ МОЩНОСТИ\'!B1+E2<=1000;"B";"⛔ Стоп")));IF(\'КОНТРОЛЬ МОЩНОСТИ\'!C1+E2<=400;"B";IF(\'КОНТРОЛЬ МОЩНОСТИ\'!A1+E2<=1000;"A";IF(\'КОНТРОЛЬ МОЩНОСТИ\'!C1+E2<=1000;"B";"⛔ Стоп"))))))'

# Update cell I2
sheet.update_acell('I2', new_formula)
print('Формула обновлена в I2')

# Copy formula down using batch update
# Generate formulas for rows 3-500
updates = []
for row in range(3, 501):
    formula = new_formula.replace('E2', f'E{row}').replace('H2', f'H{row}')
    updates.append({
        'range': f'I{row}',
        'values': [[formula]]
    })

# Batch update in chunks of 100
for i in range(0, len(updates), 100):
    chunk = updates[i:i+100]
    sheet.batch_update(chunk, value_input_option='USER_ENTERED')
    print(f'Обновлено строк: {min(i+100, len(updates))}')

print('Готово!')
