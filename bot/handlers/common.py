from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot import keyboards
from bot.locales import get_text, RU, UZ
from bot.services.sheets import get_sheets_service

router = Router()


@router.message(F.text.in_([RU["BTN_CANCEL"], UZ["BTN_CANCEL"]]))
async def cancel_action(message: Message, state: FSMContext):
    """Cancel current action and return to main menu"""
    user_id = message.from_user.id
    data = await state.get_data()

    # If there's a draft order, delete it
    if 'row_number' in data:
        try:
            sheets_service = get_sheets_service()
            sheets_service.delete_draft(data['row_number'])
        except Exception:
            pass  # Ignore errors on cleanup

    await state.clear()
    await message.answer(
        get_text(user_id, "START_MESSAGE"),
        reply_markup=keyboards.main_menu_kb(user_id)
    )
