import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sh = gc.open_by_key("1RGvQfkcEOCZj905MYi0O2h9DRUMtFXNZbQ_SR6-gcbo")
settings = sh.worksheet("НАСТРОЙКИ")

# Add new columns for working hours
# F: Начало работы (10:00)
# G: Конец работы (20:00)
# H: Часов в день (формула)
# I: Листов в час (формула)

# Update headers
settings.update_acell("F1", "Начало работы")
settings.update_acell("G1", "Конец работы")
settings.update_acell("H1", "Часов в день")
settings.update_acell("I1", "Листов в час")

# Update values for row 2
settings.update_acell("F2", "10:00")
settings.update_acell("G2", "20:00")
settings.update_acell("H2", "=HOUR(G2)-HOUR(F2)")  # 10 hours
settings.update_acell("I2", "=A2/H2")  # 20 sheets per hour

# Copy to rows 3-5 for consistency
for row in range(3, 6):
    settings.update_acell(f"F{row}", "10:00")
    settings.update_acell(f"G{row}", "20:00")
    settings.update_acell(f"H{row}", f"=HOUR(G{row})-HOUR(F{row})")
    settings.update_acell(f"I{row}", f"=A{row}/H{row}")

print("Настройки обновлены!")
print("F: Начало работы = 10:00")
print("G: Конец работы = 20:00")
print("H: Часов в день = 10")
print("I: Листов в час = 20")
