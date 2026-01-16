"""Localization system for bot messages"""

# Store user language preferences (telegram_id -> language)
_user_languages: dict[int, str] = {}


def set_user_language(user_id: int, lang: str):
    """Set user's preferred language"""
    _user_languages[user_id] = lang


def get_user_language(user_id: int) -> str:
    """Get user's preferred language, default to Russian"""
    return _user_languages.get(user_id, "ru")


# === RUSSIAN TEXTS ===
RU = {
    # Language selection
    "SELECT_LANGUAGE": "Выберите язык / Tilni tanlang:",

    # Start menu
    "START_MESSAGE": """Добро пожаловать!

Я помогу:
- оформить заказ
- узнать статус
- увидеть дату готовности""",

    # New order flow
    "ASK_CLIENT_TYPE": "Кто вы?",
    "ASK_BRANCH": "Выберите филиал:",
    "ASK_CLIENT_NAME": "Напишите ваше имя:",
    "ASK_DELIVERY": "Как вы планируете получить заказ?",
    "ASK_SHEETS": "Введите количество листов (числом):",
    "INVALID_SHEETS": "Пожалуйста, введите корректное число (больше 0):",
    "ASK_FILE": "Прикрепите файл для печати:",

    # Capacity check
    "CAPACITY_OVERLOAD": """Производство сейчас загружено.

Ближайшая возможная дата:
{date}

Попробуйте позже или свяжитесь с менеджером.""",

    # Order confirmation
    "ORDER_CONFIRMED": """Заказ принят!

№ {order_number}
Листов: {sheets}
Станок: {machine}

Дата готовности — в разделе «Мои заказы»""",

    # My orders
    "NO_ORDERS": "У вас пока нет заказов.",
    "SELECT_ORDER": "Ваши заказы:",
    "ORDER_CARD": """Заказ #{order_number}

Статус: {status}
Листов: {sheets}
Станок: {machine}
Дата готовности: {ready_date}""",

    # Rules
    "RULES_TEXT": """Как мы работаем:

- Срок считается с момента подтверждения заказа
- Максимальный срок — 5 рабочих дней
- Срочные заказы — отдельная услуга
- Новый файл = новый заказ
- Очередь формируется автоматически""",

    # Contact
    "CONTACT_TEXT": """Контакт менеджера:
{contact}

Время работы:
Пн–Сб 09:00–18:00""",

    # Buttons
    "BTN_NEW_ORDER": "Новый заказ",
    "BTN_MY_ORDERS": "Мои заказы",
    "BTN_RULES": "Правила и сроки",
    "BTN_CONTACT": "Связаться с менеджером",
    "BTN_CLIENT": "Клиент",
    "BTN_BRANCH": "Филиал",
    "BTN_PICKUP": "Самовывоз",
    "BTN_DELIVERY": "Доставка",
    "BTN_TRY_LATER": "Попробовать позже",
    "BTN_ACCEPT_DATE": "Согласен на эту дату",
    "BTN_MANAGER": "Менеджер",
    "BTN_REFRESH": "Обновить статус",
    "BTN_BACK": "Назад",
    "BTN_MAIN_MENU": "Главное меню",
    "BTN_CANCEL": "Отмена",
    "BTN_DELETE": "Удалить из списка",

    # System messages
    "CHECKING_CAPACITY": "Проверяю доступность...",
    "ERROR_CHECK": "Ошибка при проверке: {error}\nПопробуйте позже.",
    "ERROR_SAVE": "Ошибка при сохранении заказа: {error}\nСвяжитесь с менеджером.",
    "ERROR_LOAD": "Ошибка при загрузке заказов: {error}",
    "ORDER_NOT_FOUND": "Заказ не найден",
    "UPDATED": "Обновлено",
    "ERROR_SHORT": "Ошибка: {error}",
    "ORDER_DELETED": "Заказ удалён из списка",
    "CONFIRM_DELETE": "Удалить заказ #{order_number} из списка?",
    "BTN_CONFIRM_DELETE": "Да, удалить",
}

# === UZBEK TEXTS ===
UZ = {
    # Language selection
    "SELECT_LANGUAGE": "Выберите язык / Tilni tanlang:",

    # Start menu
    "START_MESSAGE": """Xush kelibsiz!

Men yordam beraman:
- buyurtma berish
- holatni bilish
- tayyor bo'lish sanasini ko'rish""",

    # New order flow
    "ASK_CLIENT_TYPE": "Siz kimsiz?",
    "ASK_BRANCH": "Filialni tanlang:",
    "ASK_CLIENT_NAME": "Ismingizni yozing:",
    "ASK_DELIVERY": "Buyurtmani qanday olasiz?",
    "ASK_SHEETS": "Varaqlar sonini kiriting (raqam bilan):",
    "INVALID_SHEETS": "Iltimos, to'g'ri raqam kiriting (0 dan katta):",
    "ASK_FILE": "Chop etish uchun faylni biriktiring:",

    # Capacity check
    "CAPACITY_OVERLOAD": """Ishlab chiqarish hozirda band.

Eng yaqin mumkin bo'lgan sana:
{date}

Keyinroq urinib ko'ring yoki menejer bilan bog'laning.""",

    # Order confirmation
    "ORDER_CONFIRMED": """Buyurtma qabul qilindi!

№ {order_number}
Varaqlar: {sheets}
Stanok: {machine}

Tayyor bo'lish sanasi — «Mening buyurtmalarim» bo'limida""",

    # My orders
    "NO_ORDERS": "Sizda hali buyurtmalar yo'q.",
    "SELECT_ORDER": "Sizning buyurtmalaringiz:",
    "ORDER_CARD": """Buyurtma #{order_number}

Holat: {status}
Varaqlar: {sheets}
Stanok: {machine}
Tayyor bo'lish sanasi: {ready_date}""",

    # Rules
    "RULES_TEXT": """Biz qanday ishlaymiz:

- Muddat buyurtma tasdiqlangan paytdan boshlab hisoblanadi
- Maksimal muddat — 5 ish kuni
- Shoshilinch buyurtmalar — alohida xizmat
- Yangi fayl = yangi buyurtma
- Navbat avtomatik ravishda shakllanadi""",

    # Contact
    "CONTACT_TEXT": """Menejer kontakti:
{contact}

Ish vaqti:
Du–Sha 09:00–18:00""",

    # Buttons
    "BTN_NEW_ORDER": "Yangi buyurtma",
    "BTN_MY_ORDERS": "Mening buyurtmalarim",
    "BTN_RULES": "Qoidalar va muddatlar",
    "BTN_CONTACT": "Menejer bilan bog'lanish",
    "BTN_CLIENT": "Mijoz",
    "BTN_BRANCH": "Filial",
    "BTN_PICKUP": "O'zi olib ketish",
    "BTN_DELIVERY": "Yetkazib berish",
    "BTN_TRY_LATER": "Keyinroq urinish",
    "BTN_ACCEPT_DATE": "Bu sanaga roziman",
    "BTN_MANAGER": "Menejer",
    "BTN_REFRESH": "Holatni yangilash",
    "BTN_BACK": "Orqaga",
    "BTN_MAIN_MENU": "Asosiy menyu",
    "BTN_CANCEL": "Bekor qilish",
    "BTN_DELETE": "Ro'yxatdan o'chirish",

    # System messages
    "CHECKING_CAPACITY": "Mavjudlikni tekshiryapman...",
    "ERROR_CHECK": "Tekshirishda xato: {error}\nKeyinroq urinib ko'ring.",
    "ERROR_SAVE": "Buyurtmani saqlashda xato: {error}\nMenejer bilan bog'laning.",
    "ERROR_LOAD": "Buyurtmalarni yuklashda xato: {error}",
    "ORDER_NOT_FOUND": "Buyurtma topilmadi",
    "UPDATED": "Yangilandi",
    "ERROR_SHORT": "Xato: {error}",
    "ORDER_DELETED": "Buyurtma ro'yxatdan o'chirildi",
    "CONFIRM_DELETE": "Buyurtma #{order_number} ni ro'yxatdan o'chirishni xohlaysizmi?",
    "BTN_CONFIRM_DELETE": "Ha, o'chirish",
}

# Language dictionaries
LANGUAGES = {
    "ru": RU,
    "uz": UZ,
}


def get_text(user_id: int, key: str) -> str:
    """Get localized text for user"""
    lang = get_user_language(user_id)
    return LANGUAGES.get(lang, RU).get(key, RU.get(key, key))


def get_texts(user_id: int) -> dict:
    """Get all texts for user's language"""
    lang = get_user_language(user_id)
    return LANGUAGES.get(lang, RU)
