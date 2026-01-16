from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot import keyboards
from bot.states import OrderStates
from bot.locales import get_text, set_user_language, get_user_language, RU, UZ

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command - show language selection"""
    await state.clear()
    await message.answer(
        "Выберите язык / Tilni tanlang:",
        reply_markup=keyboards.language_kb()
    )


@router.callback_query(F.data.startswith("lang:"))
async def process_language(callback: CallbackQuery, state: FSMContext):
    """Process language selection"""
    lang = callback.data.split(":")[1]
    user_id = callback.from_user.id

    set_user_language(user_id, lang)

    await callback.message.edit_text(
        get_text(user_id, "START_MESSAGE")
    )
    await callback.message.answer(
        get_text(user_id, "START_MESSAGE"),
        reply_markup=keyboards.main_menu_kb(user_id)
    )
    await callback.answer()


@router.message(F.text.in_([RU["BTN_NEW_ORDER"], UZ["BTN_NEW_ORDER"]]))
async def start_new_order(message: Message, state: FSMContext):
    """Start new order flow"""
    user_id = message.from_user.id
    await state.set_state(OrderStates.waiting_client_type)
    await message.answer(
        get_text(user_id, "ASK_CLIENT_TYPE"),
        reply_markup=keyboards.client_type_kb(user_id)
    )


@router.callback_query(F.data == "action:main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """Return to main menu"""
    user_id = callback.from_user.id
    await state.clear()
    await callback.message.answer(
        get_text(user_id, "START_MESSAGE"),
        reply_markup=keyboards.main_menu_kb(user_id)
    )
    await callback.answer()


@router.callback_query(F.data == "action:new_order")
async def inline_new_order(callback: CallbackQuery, state: FSMContext):
    """Start new order from inline button"""
    user_id = callback.from_user.id
    await state.set_state(OrderStates.waiting_client_type)
    await callback.message.answer(
        get_text(user_id, "ASK_CLIENT_TYPE"),
        reply_markup=keyboards.client_type_kb(user_id)
    )
    await callback.answer()


@router.callback_query(F.data == "action:try_later")
async def try_later(callback: CallbackQuery, state: FSMContext):
    """User wants to try later after overload (fallback handler)"""
    from bot.services.sheets import get_sheets_service
    user_id = callback.from_user.id
    data = await state.get_data()

    # Delete draft if exists
    if 'row_number' in data:
        try:
            sheets_service = get_sheets_service()
            sheets_service.delete_draft(data['row_number'])
        except Exception:
            pass

    await state.clear()
    await callback.message.answer(
        get_text(user_id, "START_MESSAGE"),
        reply_markup=keyboards.main_menu_kb(user_id)
    )
    await callback.answer()
