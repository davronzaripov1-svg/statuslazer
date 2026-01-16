from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from bot.locales import get_text


# === Language Selection ===

def language_kb() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang:uz"),
            ]
        ]
    )


# === Reply Keyboards ===

def main_menu_kb(user_id: int) -> ReplyKeyboardMarkup:
    """Main menu keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(user_id, "BTN_NEW_ORDER"))],
            [KeyboardButton(text=get_text(user_id, "BTN_MY_ORDERS"))],
            [KeyboardButton(text=get_text(user_id, "BTN_RULES"))],
            [KeyboardButton(text=get_text(user_id, "BTN_CONTACT"))],
        ],
        resize_keyboard=True
    )


def cancel_kb(user_id: int) -> ReplyKeyboardMarkup:
    """Cancel button during order flow"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(user_id, "BTN_CANCEL"))],
        ],
        resize_keyboard=True
    )


# === Inline Keyboards ===

def client_type_kb(user_id: int) -> InlineKeyboardMarkup:
    """Client type selection"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"👤 {get_text(user_id, 'BTN_CLIENT')}",
                    callback_data="client_type:client"
                ),
                InlineKeyboardButton(
                    text=f"🏢 {get_text(user_id, 'BTN_BRANCH')}",
                    callback_data="client_type:branch"
                ),
            ]
        ]
    )


# Branch names list
BRANCHES = [
    "Наманган",
    "Коканд",
    "Андижан",
    "Самарканд",
    "ДФТ",
    "СтаутсПринт",
    "Казахстан",
    "Таджикистан",
]


def branch_kb() -> InlineKeyboardMarkup:
    """Branch selection keyboard"""
    buttons = []
    for branch in BRANCHES:
        buttons.append([
            InlineKeyboardButton(
                text=f"🏢 {branch}",
                callback_data=f"branch:{branch}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def delivery_kb(user_id: int) -> InlineKeyboardMarkup:
    """Delivery method selection"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🚶 {get_text(user_id, 'BTN_PICKUP')}",
                    callback_data="delivery:pickup"
                ),
                InlineKeyboardButton(
                    text=f"🚚 {get_text(user_id, 'BTN_DELIVERY')}",
                    callback_data="delivery:delivery"
                ),
            ]
        ]
    )


def overload_kb(user_id: int) -> InlineKeyboardMarkup:
    """Keyboard shown when capacity is exceeded"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"✅ {get_text(user_id, 'BTN_ACCEPT_DATE')}",
                    callback_data="action:accept_date"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🔄 {get_text(user_id, 'BTN_TRY_LATER')}",
                    callback_data="action:try_later"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"📞 {get_text(user_id, 'BTN_MANAGER')}",
                    callback_data="action:contact"
                ),
            ]
        ]
    )


def order_confirmed_kb(user_id: int) -> InlineKeyboardMarkup:
    """Keyboard after order confirmation"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"📦 {get_text(user_id, 'BTN_MY_ORDERS')}",
                    callback_data="action:my_orders"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🆕 {get_text(user_id, 'BTN_NEW_ORDER')}",
                    callback_data="action:new_order"
                ),
            ]
        ]
    )


def orders_list_kb(user_id: int, orders: list[tuple[int, str]]) -> InlineKeyboardMarkup:
    """List of user orders. orders = [(order_number, status), ...]"""
    buttons = []
    for order_num, status in orders:
        buttons.append([
            InlineKeyboardButton(
                text=f"📦 #{order_num}",
                callback_data=f"order:{order_num}"
            )
        ])
    buttons.append([
        InlineKeyboardButton(
            text=f"🏠 {get_text(user_id, 'BTN_MAIN_MENU')}",
            callback_data="action:main_menu"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def order_card_kb(user_id: int, order_number: int) -> InlineKeyboardMarkup:
    """Single order card keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🔄 {get_text(user_id, 'BTN_REFRESH')}",
                    callback_data=f"refresh:{order_number}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🗑 {get_text(user_id, 'BTN_DELETE')}",
                    callback_data=f"delete:{order_number}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"📞 {get_text(user_id, 'BTN_MANAGER')}",
                    callback_data="action:contact"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"⬅️ {get_text(user_id, 'BTN_BACK')}",
                    callback_data="action:my_orders"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🏠 {get_text(user_id, 'BTN_MAIN_MENU')}",
                    callback_data="action:main_menu"
                ),
            ]
        ]
    )


def confirm_delete_kb(user_id: int, order_number: int) -> InlineKeyboardMarkup:
    """Confirm delete order keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"✅ {get_text(user_id, 'BTN_CONFIRM_DELETE')}",
                    callback_data=f"confirm_delete:{order_number}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"⬅️ {get_text(user_id, 'BTN_BACK')}",
                    callback_data=f"order:{order_number}"
                ),
            ]
        ]
    )


def back_kb(user_id: int) -> InlineKeyboardMarkup:
    """Simple back button"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"⬅️ {get_text(user_id, 'BTN_BACK')}",
                    callback_data="action:main_menu"
                ),
            ]
        ]
    )


def production_status_kb(order_number: int, current_status: str = "") -> InlineKeyboardMarkup:
    """Status buttons for production group"""
    def label(status: str, emoji: str, text: str) -> str:
        if current_status == status:
            return f"✓ {emoji} {text}"
        return f"{emoji} {text}"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=label("В очереди", "📋", "В очереди"),
                    callback_data=f"status:{order_number}:В очереди"
                ),
                InlineKeyboardButton(
                    text=label("В работе", "🔧", "В работе"),
                    callback_data=f"status:{order_number}:В работе"
                ),
                InlineKeyboardButton(
                    text=label("Готов", "✅", "Готов"),
                    callback_data=f"status:{order_number}:Готов"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=label("Отклонён", "❌", "Отклонён"),
                    callback_data=f"status:{order_number}:Отклонён"
                ),
                InlineKeyboardButton(
                    text=label("Отправлен", "🚚", "Отправлен"),
                    callback_data=f"status:{order_number}:Отправлен"
                ),
            ]
        ]
    )
