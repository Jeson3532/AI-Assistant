# src/frontend/bot/routers/message/operator.py

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from src.frontend.bot.fsm.groups import Operator
from src.frontend.bot.storage import tickets as ticket_store
from src.frontend.bot.templates import messages as tpl

router = Router(name='Operator Message Router')


@router.message(Command("close"), Operator.HANDLE_TICKET)
async def close_ticket(msg: Message, state: FSMContext, bot: Bot):
    ticket = ticket_store.get_ticket_by_operator(msg.from_user.id)
    if not ticket:
        await msg.answer("Активный тикет не найден.")
        return

    history_text = "\n".join([
        f"{'👤' if m['role'] == 'user' else '🧑‍💼'} {m['text']}"
        for m in ticket.history
    ])

    user_id = ticket.user_id
    ticket_store.close_ticket(ticket)
    await state.clear()

    await msg.answer(
        f"{tpl.OPERATOR_TICKET_CLOSED}\n\n<b>История диалога:</b>\n{history_text}", parse_mode="html"
    )
    await bot.send_message(user_id, tpl.USER_OPERATOR_CLOSED, parse_mode='html')


@router.message(Operator.HANDLE_TICKET)
async def operator_reply(msg: Message, bot: Bot):
    ticket = ticket_store.get_ticket_by_operator(msg.from_user.id)
    if not ticket:
        await msg.answer("Активный тикет не найден.")
        return
    ticket.history.append({"role": "operator", "text": msg.text})
    await bot.send_message(ticket.user_id,
                           f"💬 <b>Сообщение от оператора</b>:\n<code>{msg.text}</code>",
                           parse_mode="html")
