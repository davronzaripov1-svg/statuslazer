from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from bot import texts, keyboards
from bot.config import PRODUCTION_GROUP_ID, TOPIC_BRANCH, TOPIC_CLIENT
from bot.services.sheets import get_sheets_service

router = Router()


async def send_order_to_production(
    bot: Bot,
    order_number: int,
    client_type: str,
    sheets_count: int,
    delivery: str,
    machine: str,
    ready_date: str,
    status: str = "В очереди",
    file_id: str = None,
    is_photo: bool = False
):
    """Send order notification to production group"""
    # Determine which topic to send to
    if "Филиал" in client_type:
        topic_id = TOPIC_BRANCH
    else:
        topic_id = TOPIC_CLIENT

    message_text = texts.PRODUCTION_ORDER.format(
        order_number=order_number,
        client_type=client_type,
        sheets=sheets_count,
        delivery=delivery,
        machine=machine,
        ready_date=ready_date,
        status=status
    )

    # Send file first if provided
    if file_id:
        if is_photo:
            await bot.send_photo(
                chat_id=PRODUCTION_GROUP_ID,
                message_thread_id=topic_id,
                photo=file_id,
                caption=message_text,
                reply_markup=keyboards.production_status_kb(order_number, status)
            )
        else:
            await bot.send_document(
                chat_id=PRODUCTION_GROUP_ID,
                message_thread_id=topic_id,
                document=file_id,
                caption=message_text,
                reply_markup=keyboards.production_status_kb(order_number, status)
            )
    else:
        await bot.send_message(
            chat_id=PRODUCTION_GROUP_ID,
            message_thread_id=topic_id,
            text=message_text,
            reply_markup=keyboards.production_status_kb(order_number, status)
        )


@router.callback_query(F.data.startswith("status:"))
async def update_order_status(callback: CallbackQuery):
    """Handle status button click in production group"""
    # Parse callback data: status:order_number:new_status
    parts = callback.data.split(":", 2)
    if len(parts) != 3:
        await callback.answer("Ошибка данных")
        return

    _, order_number_str, new_status = parts

    try:
        order_number = int(order_number_str)
    except ValueError:
        await callback.answer("Неверный номер заказа")
        return

    # Update status in Google Sheets
    try:
        sheets_service = get_sheets_service()
        sheets_service.update_order_status(order_number, new_status)

        # Get the text - either from message.text or message.caption (for photos/docs)
        old_text = callback.message.text or callback.message.caption or ""
        lines = old_text.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith("Статус:"):
                new_lines.append(f"Статус: {new_status}")
            else:
                new_lines.append(line)
        new_text = '\n'.join(new_lines)

        # Edit caption if it's a photo/document, otherwise edit text
        if callback.message.photo or callback.message.document:
            await callback.message.edit_caption(
                caption=new_text,
                reply_markup=keyboards.production_status_kb(order_number, new_status)
            )
        else:
            await callback.message.edit_text(
                text=new_text,
                reply_markup=keyboards.production_status_kb(order_number, new_status)
            )

        await callback.answer(f"Статус изменён: {new_status}")

    except Exception as e:
        await callback.answer(f"Ошибка: {e}", show_alert=True)
