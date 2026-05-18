from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from src.frontend.bot.fsm.groups import Operator
from src.frontend.bot.storage import tickets as ticket_store
from src.frontend.bot.templates import messages as tpl
from src.frontend.bot.utils.log import logger
from src.frontend.bot.utils.request import upload_doc

router = Router(name='Operator Callback Router')


@router.callback_query(F.data.startswith("accept_ticket:"))
async def accept_ticket(cb: CallbackQuery, state: FSMContext, bot: Bot):
    ticket_id = int(cb.data.split(":")[1])
    ticket = ticket_store.tickets.get(ticket_id)

    if not ticket or ticket.status != "pending":
        await cb.answer("Тикет уже принят другим оператором", show_alert=True)
        await cb.message.edit_reply_markup(reply_markup=None)
        return

    ticket.operator_id = cb.from_user.id
    ticket.status = "in_progress"
    ticket_store.operator_to_ticket[cb.from_user.id] = ticket_id

    for op_id, msg_id in ticket.operator_notify_msgs.items():
        if op_id != cb.from_user.id:
            try:
                await bot.edit_message_reply_markup(
                    chat_id=op_id,
                    message_id=msg_id,
                    reply_markup=None
                )
            except Exception:
                pass

    await state.set_state(Operator.HANDLE_TICKET)
    await cb.answer("Тикет принят!")
    await cb.message.edit_text(
        tpl.operator_ticket_accepted(ticket_id),
        reply_markup=None,
        parse_mode='html'
    )

    await bot.send_message(ticket.user_id, tpl.USER_OPERATOR_CONNECTED, parse_mode='html')


@router.callback_query(F.data.startswith("save_kb_"))
async def save_to_knowledge_base(cb: CallbackQuery):
    await cb.answer()
    ticket_id = int(cb.data.split("_")[-1])
    ticket = ticket_store.tickets.get(ticket_id)

    if not ticket:
        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.message.answer("⚠️ Тикет не найден — возможно, бот был перезапущен.")
        return

    try:
        content = "\n".join([m["text"] for m in ticket.history])
        await upload_doc(
            title=f"ticket_{ticket.ticket_id}_{ticket.dialog_type}",
            content=content,
            dialog_type=ticket.dialog_type,
        )
        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.message.answer("✅ Диалог сохранён в базу знаний.")
    except Exception as e:
        logger.error(f"Ошибка сохранения в KB: {e}")
        await cb.message.answer("❌ Не удалось сохранить. Попробуйте позже.")


@router.callback_query(F.data == "ticket_taken")
async def ticket_taken(cb: CallbackQuery):
    await cb.answer("Этот тикет уже обработан", show_alert=True)
