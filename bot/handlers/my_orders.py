from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot import keyboards
from bot.locales import get_text, RU, UZ
from bot.states import MyOrdersStates
from bot.services.sheets import get_sheets_service

router = Router()


@router.message(F.text.in_([RU["BTN_MY_ORDERS"], UZ["BTN_MY_ORDERS"]]))
async def show_my_orders(message: Message, state: FSMContext):
    """Show user's orders list"""
    user_id = message.from_user.id
    await state.set_state(MyOrdersStates.viewing_list)

    try:
        sheets_service = get_sheets_service()
        orders = sheets_service.get_user_orders(user_id)

        if not orders:
            await state.clear()
            await message.answer(
                get_text(user_id, "NO_ORDERS"),
                reply_markup=keyboards.main_menu_kb(user_id)
            )
            return

        orders_list = [(o.order_number, o.status) for o in orders]
        await message.answer(
            get_text(user_id, "SELECT_ORDER"),
            reply_markup=keyboards.orders_list_kb(user_id, orders_list)
        )

    except Exception as e:
        await message.answer(get_text(user_id, "ERROR_LOAD").format(error=str(e)))
        await state.clear()


@router.callback_query(F.data == "action:my_orders")
async def inline_my_orders(callback: CallbackQuery, state: FSMContext):
    """Show user's orders from inline button"""
    user_id = callback.from_user.id
    await state.set_state(MyOrdersStates.viewing_list)

    try:
        sheets_service = get_sheets_service()
        orders = sheets_service.get_user_orders(user_id)

        if not orders:
            await state.clear()
            await callback.message.answer(
                get_text(user_id, "NO_ORDERS"),
                reply_markup=keyboards.main_menu_kb(user_id)
            )
            await callback.answer()
            return

        orders_list = [(o.order_number, o.status) for o in orders]
        await callback.message.answer(
            get_text(user_id, "SELECT_ORDER"),
            reply_markup=keyboards.orders_list_kb(user_id, orders_list)
        )
        await callback.answer()

    except Exception as e:
        await callback.message.answer(get_text(user_id, "ERROR_LOAD").format(error=str(e)))
        await callback.answer()
        await state.clear()


@router.callback_query(F.data.startswith("order:"))
async def show_order_card(callback: CallbackQuery, state: FSMContext):
    """Show single order details"""
    user_id = callback.from_user.id
    order_number = int(callback.data.split(":")[1])
    await state.set_state(MyOrdersStates.viewing_card)
    await state.update_data(current_order=order_number)

    try:
        sheets_service = get_sheets_service()
        order = sheets_service.get_order_by_number(order_number, user_id)

        if not order:
            await callback.answer(get_text(user_id, "ORDER_NOT_FOUND"), show_alert=True)
            return

        await callback.message.edit_text(
            get_text(user_id, "ORDER_CARD").format(
                order_number=order.order_number,
                status=order.status,
                sheets=order.sheets_count,
                machine=order.machine,
                ready_date=order.ready_date
            ),
            reply_markup=keyboards.order_card_kb(user_id, order.order_number)
        )
        await callback.answer()

    except Exception as e:
        await callback.answer(get_text(user_id, "ERROR_SHORT").format(error=str(e)), show_alert=True)


@router.callback_query(F.data.startswith("refresh:"))
async def refresh_order(callback: CallbackQuery, state: FSMContext):
    """Refresh order status"""
    user_id = callback.from_user.id
    order_number = int(callback.data.split(":")[1])

    try:
        sheets_service = get_sheets_service()
        order = sheets_service.get_order_by_number(order_number, user_id)

        if not order:
            await callback.answer(get_text(user_id, "ORDER_NOT_FOUND"), show_alert=True)
            return

        await callback.message.edit_text(
            get_text(user_id, "ORDER_CARD").format(
                order_number=order.order_number,
                status=order.status,
                sheets=order.sheets_count,
                machine=order.machine,
                ready_date=order.ready_date
            ),
            reply_markup=keyboards.order_card_kb(user_id, order.order_number)
        )
        await callback.answer(get_text(user_id, "UPDATED"))

    except Exception as e:
        await callback.answer(get_text(user_id, "ERROR_SHORT").format(error=str(e)), show_alert=True)


@router.callback_query(F.data.startswith("delete:"))
async def ask_delete_order(callback: CallbackQuery, state: FSMContext):
    """Ask confirmation before deleting order from list"""
    user_id = callback.from_user.id
    order_number = int(callback.data.split(":")[1])

    await callback.message.edit_text(
        get_text(user_id, "CONFIRM_DELETE").format(order_number=order_number),
        reply_markup=keyboards.confirm_delete_kb(user_id, order_number)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_delete:"))
async def confirm_delete_order(callback: CallbackQuery, state: FSMContext):
    """Delete order from user's list"""
    user_id = callback.from_user.id
    order_number = int(callback.data.split(":")[1])

    try:
        sheets_service = get_sheets_service()
        success = sheets_service.hide_order_from_user(order_number, user_id)

        if success:
            await callback.answer(get_text(user_id, "ORDER_DELETED"), show_alert=True)
            # Return to orders list
            orders = sheets_service.get_user_orders(user_id)
            if orders:
                orders_list = [(o.order_number, o.status) for o in orders]
                await callback.message.edit_text(
                    get_text(user_id, "SELECT_ORDER"),
                    reply_markup=keyboards.orders_list_kb(user_id, orders_list)
                )
            else:
                await callback.message.edit_text(get_text(user_id, "NO_ORDERS"))
                await state.clear()
        else:
            await callback.answer(get_text(user_id, "ORDER_NOT_FOUND"), show_alert=True)

    except Exception as e:
        await callback.answer(get_text(user_id, "ERROR_SHORT").format(error=str(e)), show_alert=True)
