"""All bot messages in Russian"""

# Start menu
START_MESSAGE = """Добро пожаловать!

Я помогу:
- оформить заказ
- узнать статус
- увидеть дату готовности"""

# New order flow
ASK_CLIENT_TYPE = "Кто вы?"
ASK_DELIVERY = "Как вы планируете получить заказ?"
ASK_SHEETS = "Введите количество листов (числом):"
INVALID_SHEETS = "Пожалуйста, введите корректное число (больше 0):"
ASK_FILE = "Прикрепите файл для печати:"

# Capacity check
CAPACITY_OVERLOAD = """Производство сейчас загружено.

Ближайшая возможная дата:
{date}

Попробуйте позже или свяжитесь с менеджером."""

# Order confirmation
ORDER_CONFIRMED = """Заказ принят!

№ {order_number}
Листов: {sheets}
Станок: {machine}

Дата готовности — в разделе «Мои заказы»"""

# My orders
NO_ORDERS = "У вас пока нет заказов."
SELECT_ORDER = "Ваши заказы:"

ORDER_CARD = """Заказ #{order_number}

Статус: {status}
Листов: {sheets}
Станок: {machine}
Дата готовности: {ready_date}"""

# Rules
RULES_TEXT = """Как мы работаем:

- Срок считается с момента подтверждения заказа
- Максимальный срок — 5 рабочих дней
- Срочные заказы — отдельная услуга
- Новый файл = новый заказ
- Очередь формируется автоматически"""

# Contact
CONTACT_TEXT = """Контакт менеджера:
{contact}

Время работы:
Пн–Сб 09:00–18:00"""

# Production group notification
PRODUCTION_ORDER = """Новый заказ #{order_number}

Тип: {client_type}
Листов: {sheets}
Получение: {delivery}
Станок: {machine}
Дата готовности: {ready_date}

Статус: {status}"""

# Buttons
BTN_NEW_ORDER = "Новый заказ"
BTN_MY_ORDERS = "Мои заказы"
BTN_RULES = "Правила и сроки"
BTN_CONTACT = "Связаться с менеджером"
BTN_CLIENT = "Клиент"
BTN_BRANCH = "Филиал"
BTN_PICKUP = "Самовывоз"
BTN_DELIVERY = "Доставка"
BTN_TRY_LATER = "Попробовать позже"
BTN_MANAGER = "Менеджер"
BTN_REFRESH = "Обновить статус"
BTN_BACK = "Назад"
BTN_MAIN_MENU = "Главное меню"
BTN_CANCEL = "Отмена"
