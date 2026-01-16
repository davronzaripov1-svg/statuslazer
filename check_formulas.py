import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sh = gc.open_by_key("1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo")
sheet = sh.worksheet("ЗАКАЗЫ")

# Check formulas in row 3 (next empty row)
print("=== Формулы в строке 3 ===")
formulas = sheet.get("I3:L3", value_render_option="FORMULA")
if formulas and formulas[0]:
    print(f"I3 (Рекоменд. станок): {formulas[0][0] if len(formulas[0]) > 0 else 'пусто'}")
    print(f"J3 (Листов впереди): {formulas[0][1] if len(formulas[0]) > 1 else 'пусто'}")
    print(f"K3 (Дней производства): {formulas[0][2] if len(formulas[0]) > 2 else 'пусто'}")
    print(f"L3 (Дата готовности): {formulas[0][3] if len(formulas[0]) > 3 else 'пусто'}")
else:
    print("Формулы не найдены в строке 3")

# Check row 2 formula for L
print("\n=== Формула L2 ===")
l2_formula = sheet.get("L2", value_render_option="FORMULA")
print(f"L2: {l2_formula}")

# Check НАСТРОЙКИ for daily capacity
print("\n=== НАСТРОЙКИ ===")
settings = sh.worksheet("НАСТРОЙКИ")
a2 = settings.acell("A2").value
print(f"Листов в день (A2): {a2}")
