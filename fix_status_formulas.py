import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sh = gc.open_by_key("1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo")
sheet = sh.worksheet("ЗАКАЗЫ")

# Update J formula to exclude "Готов", "Отправлен", "Отклонён"
# Using SUMPRODUCT instead of SUMIFS for multiple OR conditions
# Finished statuses: Готов, Отправлен, Отклонён

# New formula for J2 - sheets ahead in queue (excluding finished orders)
j_formula = '=SUMPRODUCT(($F$2:$F<>"Готов")*($F$2:$F<>"Отправлен")*($F$2:$F<>"Отклонён")*($G$2:$G=G2)*($H$2:$H=H2)*($B$2:$B<=B2)*($E$2:$E))-IF(AND(F2<>"Готов";F2<>"Отправлен";F2<>"Отклонён");E2;0)'

sheet.update_acell('J2', j_formula)
print('Формула J2 обновлена')

# Copy to remaining rows
updates = []
for row in range(3, 501):
    formula = j_formula.replace('G2', f'G{row}').replace('H2', f'H{row}').replace('B2', f'B{row}').replace('E2', f'E{row}').replace('F2', f'F{row}')
    updates.append({
        'range': f'J{row}',
        'values': [[formula]]
    })

for i in range(0, len(updates), 100):
    chunk = updates[i:i+100]
    sheet.batch_update(chunk, value_input_option='USER_ENTERED')
    print(f'J обновлено: {min(i+100, len(updates))} строк')

# Also update КОНТРОЛЬ МОЩНОСТИ sheet
print()
print('Обновляю КОНТРОЛЬ МОЩНОСТИ...')
cap = sh.worksheet('КОНТРОЛЬ МОЩНОСТИ')

# Update formulas to exclude finished statuses
# A1: Machine A load
cap.update_acell('A1', '=SUMPRODUCT((\'ЗАКАЗЫ\'!$F:$F<>"Готов")*(\'ЗАКАЗЫ\'!$F:$F<>"Отправлен")*(\'ЗАКАЗЫ\'!$F:$F<>"Отклонён")*(\'ЗАКАЗЫ\'!$G:$G="A")*(\'ЗАКАЗЫ\'!$E:$E))')
print('A1 обновлена')

# B1: Machine B (Самовывоз)
cap.update_acell('B1', '=SUMPRODUCT((\'ЗАКАЗЫ\'!$F:$F<>"Готов")*(\'ЗАКАЗЫ\'!$F:$F<>"Отправлен")*(\'ЗАКАЗЫ\'!$F:$F<>"Отклонён")*(\'ЗАКАЗЫ\'!$G:$G="B")*(\'ЗАКАЗЫ\'!$H:$H="Самовывоз")*(\'ЗАКАЗЫ\'!$E:$E))')
print('B1 обновлена')

# C1: Machine B (Доставка)
cap.update_acell('C1', '=SUMPRODUCT((\'ЗАКАЗЫ\'!$F:$F<>"Готов")*(\'ЗАКАЗЫ\'!$F:$F<>"Отправлен")*(\'ЗАКАЗЫ\'!$F:$F<>"Отклонён")*(\'ЗАКАЗЫ\'!$G:$G="B")*(\'ЗАКАЗЫ\'!$H:$H="Доставка")*(\'ЗАКАЗЫ\'!$E:$E))')
print('C1 обновлена')

print()
print('Готово! Теперь статусы "Готов", "Отправлен", "Отклонён" не учитываются в очереди.')
