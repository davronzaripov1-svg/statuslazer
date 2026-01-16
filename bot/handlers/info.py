from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot import keyboards
from bot.locales import get_text, RU, UZ
from bot.config import MANAGER_CONTACT

router = Router()


@router.message(F.text.in_([RU["BTN_RULES"], UZ["BTN_RULES"]]))
async def show_rules(message: Message, state: FSMContext):
    """Show rules and SLA"""
    user_id = message.from_user.id
    await state.clear()
    await message.answer(
        get_text(user_id, "RULES_TEXT"),
        reply_markup=keyboards.back_kb(user_id)
    )


@router.message(F.text.in_([RU["BTN_CONTACT"], UZ["BTN_CONTACT"]]))
async def show_contact(message: Message, state: FSMContext):
    """Show manager contact"""
    user_id = message.from_user.id
    await state.clear()
    await message.answer(
        get_text(user_id, "CONTACT_TEXT").format(contact=MANAGER_CONTACT),
        reply_markup=keyboards.back_kb(user_id)
    )


@router.callback_query(F.data == "action:contact")
async def inline_contact(callback: CallbackQuery, state: FSMContext):
    """Show contact from inline button"""
    user_id = callback.from_user.id
    await state.clear()
    await callback.message.answer(
        get_text(user_id, "CONTACT_TEXT").format(contact=MANAGER_CONTACT),
        reply_markup=keyboards.back_kb(user_id)
    )
    await callback.answer()
