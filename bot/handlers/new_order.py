from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot import keyboards
from bot.locales import get_text
from bot.states import OrderStates
from bot.services.sheets import get_sheets_service
from bot.handlers.production import send_order_to_production

router = Router()


@router.callback_query(OrderStates.waiting_client_type, F.data.startswith("client_type:"))
async def process_client_type(callback: CallbackQuery, state: FSMContext):
    """Process client type selection"""
    user_id = callback.from_user.id
    client_type = callback.data.split(":")[1]

    if client_type == "branch":
        # Branch selected - ask for specific branch
        await state.update_data(client_type="Филиал")
        await state.set_state(OrderStates.waiting_branch)
        await callback.message.edit_text(
            get_text(user_id, "ASK_BRANCH"),
            reply_markup=keyboards.branch_kb()
        )
    else:
        # Client selected - ask for name
        await state.set_state(OrderStates.waiting_client_name)
        await callback.message.edit_text(get_text(user_id, "ASK_CLIENT_NAME"))
    await callback.answer()


@router.message(OrderStates.waiting_client_name)
async def process_client_name(message: Message, state: FSMContext):
    """Process client name input"""
    user_id = message.from_user.id
    client_name = message.text.strip()

    # Save client type with name (e.g., "Клиент: Иван")
    await state.update_data(client_type=f"Клиент: {client_name}")
    await state.set_state(OrderStates.waiting_delivery)

    await message.answer(
        get_text(user_id, "ASK_DELIVERY"),
        reply_markup=keyboards.delivery_kb(user_id)
    )


@router.callback_query(OrderStates.waiting_branch, F.data.startswith("branch:"))
async def process_branch(callback: CallbackQuery, state: FSMContext):
    """Process branch selection"""
    user_id = callback.from_user.id
    branch_name = callback.data.split(":", 1)[1]

    # Save branch name as client_type (e.g., "Филиал: Наманган")
    await state.update_data(client_type=f"Филиал: {branch_name}")
    await state.set_state(OrderStates.waiting_delivery)

    await callback.message.edit_text(
        get_text(user_id, "ASK_DELIVERY"),
        reply_markup=keyboards.delivery_kb(user_id)
    )
    await callback.answer()


@router.callback_query(OrderStates.waiting_delivery, F.data.startswith("delivery:"))
async def process_delivery(callback: CallbackQuery, state: FSMContext):
    """Process delivery method selection"""
    user_id = callback.from_user.id
    delivery = callback.data.split(":")[1]
    delivery_display = get_text(user_id, "BTN_PICKUP") if delivery == "pickup" else get_text(user_id, "BTN_DELIVERY")

    await state.update_data(delivery=delivery_display)
    await state.set_state(OrderStates.waiting_sheets)

    await callback.message.edit_text(get_text(user_id, "ASK_SHEETS"))
    await callback.answer()


@router.message(OrderStates.waiting_sheets)
async def process_sheets(message: Message, state: FSMContext):
    """Process sheets count input"""
    user_id = message.from_user.id

    # Validate number
    try:
        sheets_count = int(message.text.strip())
        if sheets_count <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        await message.answer(get_text(user_id, "INVALID_SHEETS"))
        return

    await state.update_data(sheets_count=sheets_count)
    await state.set_state(OrderStates.checking_capacity)

    # Show "checking" message
    checking_msg = await message.answer(get_text(user_id, "CHECKING_CAPACITY"))

    # Get user data
    data = await state.get_data()

    # Check capacity via Google Sheets
    try:
        sheets_service = get_sheets_service()
        result = sheets_service.create_draft_order(
            client_type=data['client_type'],
            delivery=data['delivery'],
            sheets_count=sheets_count,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            chat_id=message.chat.id
        )

        # Save draft data to state (for both accept and reject cases)
        await state.update_data(
            row_number=result.row_number,
            recommended_machine=result.recommended_machine,
            ready_date=result.ready_date
        )

        if not result.can_accept:
            # Capacity exceeded - show message with option to accept anyway
            await state.set_state(OrderStates.waiting_overload_decision)
            await checking_msg.edit_text(
                get_text(user_id, "CAPACITY_OVERLOAD").format(date=result.ready_date),
                reply_markup=keyboards.overload_kb(user_id)
            )
        else:
            # Can accept - ask for file
            await state.set_state(OrderStates.waiting_file)
            await checking_msg.edit_text(get_text(user_id, "ASK_FILE"))

    except Exception as e:
        await checking_msg.edit_text(get_text(user_id, "ERROR_CHECK").format(error=str(e)))
        await state.clear()


@router.callback_query(OrderStates.waiting_overload_decision, F.data == "action:accept_date")
async def accept_overload_date(callback: CallbackQuery, state: FSMContext):
    """User accepts the long wait date - continue with order"""
    user_id = callback.from_user.id
    await state.set_state(OrderStates.waiting_file)
    await callback.message.edit_text(get_text(user_id, "ASK_FILE"))
    await callback.answer()


@router.callback_query(OrderStates.waiting_overload_decision, F.data == "action:try_later")
async def reject_overload_date(callback: CallbackQuery, state: FSMContext):
    """User wants to try later - delete draft and return to menu"""
    user_id = callback.from_user.id
    data = await state.get_data()

    # Delete the draft
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


@router.message(OrderStates.waiting_file, F.document | F.photo)
async def process_file(message: Message, state: FSMContext, bot: Bot):
    """Process file upload"""
    user_id = message.from_user.id

    # Get file info
    is_photo = False
    if message.document:
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    elif message.photo:
        # Get largest photo
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        is_photo = True
    else:
        await message.answer(get_text(user_id, "ASK_FILE"))
        return

    data = await state.get_data()

    # Confirm order in Google Sheets
    try:
        sheets_service = get_sheets_service()
        order_number = sheets_service.confirm_order(
            row_number=data['row_number'],
            file_url=file_url,
            machine=data['recommended_machine']
        )

        # Send notification to production group with file
        try:
            await send_order_to_production(
                bot=bot,
                order_number=order_number,
                client_type=data['client_type'],
                sheets_count=data['sheets_count'],
                delivery=data['delivery'],
                machine=data['recommended_machine'],
                ready_date=data['ready_date'],
                status="В очереди",
                file_id=file_id,
                is_photo=is_photo
            )
        except Exception as e:
            # Log error but don't fail the order
            print(f"Failed to send to production group: {e}")

        await state.clear()

        await message.answer(
            get_text(user_id, "ORDER_CONFIRMED").format(
                order_number=order_number,
                sheets=data['sheets_count'],
                machine=data['recommended_machine']
            ),
            reply_markup=keyboards.order_confirmed_kb(user_id)
        )

    except Exception as e:
        await message.answer(get_text(user_id, "ERROR_SAVE").format(error=str(e)))
        await state.clear()


@router.message(OrderStates.waiting_file)
async def invalid_file(message: Message):
    """Handle invalid file input"""
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "ASK_FILE"))
