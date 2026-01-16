import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "Orders")
MANAGER_CONTACT = os.getenv("MANAGER_CONTACT", "+998 XX XXX XX XX")

# Production group settings
PRODUCTION_GROUP_ID = int(os.getenv("PRODUCTION_GROUP_ID", "-1003596802178"))
TOPIC_BRANCH = int(os.getenv("TOPIC_BRANCH", "2"))    # Филиалы
TOPIC_CLIENT = int(os.getenv("TOPIC_CLIENT", "4"))    # Клиенты

# Google Sheets column indices (0-based)
class Columns:
    ORDER_NUMBER = 0       # A - № заказа
    ACCEPTANCE_DATE = 1    # B - Дата принятия
    CLIENT = 2             # C - Клиент
    CLIENT_TYPE = 3        # D - Тип клиента
    SHEETS_COUNT = 4       # E - Кол-во листов
    STATUS = 5             # F - Статус
    MACHINE = 6            # G - Станок
    DELIVERY = 7           # H - Получение
    RECOMMENDED_MACHINE = 8  # I - Рекоменд. станок
    SHEETS_AHEAD = 9       # J - Листов впереди
    PRODUCTION_DAYS = 10   # K - Дней производства
    READY_DATE = 11        # L - Дата готовности
    SLA_CONTROL = 12       # M - SLA контроль
    TELEGRAM_ID = 13       # N - Telegram ID
    TELEGRAM_USERNAME = 14 # O - Telegram username
    CHAT_ID = 15           # P - Чат ID
    FILE_URL = 16          # Q - Файл (URL)
    SOURCE = 17            # R - Источник
    CREATED_BY = 18        # S - Создал
    CREATED_DATE = 19      # T - Дата создания
    CAN_ACCEPT = 20        # U - Можно принять
