from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from src.frontend.bot.storage import tickets
from src.frontend.bot.fsm.groups import Menus
from src.frontend.bot.utils.request import send_assistant_query, stream_assistant_query, save_dialog
from src.frontend.bot.keyboards import operator as kb_operator
from src.frontend.bot.templates import messages as tpl

from src.frontend.bot.config import BotConfig

router = Router(name='Assistant Message Router')
BOT_CONFIG = BotConfig()


@router.message(Command("exit"), Menus.ASSISTANT_CHAT)
async def exit_chat(msg: Message, state: FSMContext):
    data = await state.get_data()
    history: list[dict] = data.get("history", [])

    if history:
        await save_dialog(
            user_id=msg.from_user.id,
            username=msg.from_user.username,
            dialog_type=data.get("last_dialog_type"),
            operator=data.get("had_operator", False),
            history=history,
        )
    await state.clear()
    await msg.answer("🔴 | Чат завершен.")


@router.message(Menus.ASSISTANT_CHAT, F.text.startswith("/"))
async def block_commands_user(msg: Message):
    await msg.answer("⚠️ | Команды <b>недоступны</b> в режиме чата.\nДля выхода из чата используйте <b>/exit</b>",
                     parse_mode='html')


@router.message(Menus.ASSISTANT_CHAT)
async def handle_message(msg: Message, state: FSMContext):
    # логика пересылки сообщений
    ticket = tickets.get_ticket_by_user(msg.from_user.id)
    if ticket and ticket.status == "in_progress":
        ticket.history.append({"role": "user", "text": msg.text})
        await msg.bot.send_message(
            ticket.operator_id,
            f"<b>Сообщение от пользователя:</b>\n👤:<code> {msg.text}</code>",
            parse_mode='html'
        )
        return

    data = await state.get_data()
    history: list[dict] = data.get("history", [])

    status_msg = await msg.answer("🔍 Определяем тип обращения...")
    last_status = "🔍 Определяем тип обращения..."
    response = None

    async for event in stream_assistant_query(msg.text, history):
        if event['type'] == 'status':
            new_status = event['text']
            if new_status != last_status:
                try:
                    await status_msg.edit_text(new_status, parse_mode="html")
                    last_status = new_status
                except TelegramBadRequest:
                    ...

        elif event['type'] == 'result':
            response = event

    if not response:
        await status_msg.edit_text("❌ Что-то пошло не так. Попробуйте ещё раз.", parse_mode="html")
        return
    # запрос
    # response = await send_assistant_query(msg.text, history)
    answer = response['model_response']

    await status_msg.delete()
    await msg.answer(answer)

    history.append({"role": "user", "text": msg.text})
    history.append({"role": "assistant", "text": answer})
    await state.update_data(
        history=history,
        last_dialog_type=response.get("dialog_type"),
        had_operator=response.get("operator", False) or data.get("had_operator", False)
    )

    # создание тикета если есть вызов оператора
    if response.get('operator'):
        ticket = tickets.create_ticket(
            user_id=msg.from_user.id,
            query=msg.text,
            dialog_type=response.get('dialog_type')
        )

        # уведомление операторов
        for id_ in BOT_CONFIG.OPERATOR_IDS:
            sent = await msg.bot.send_message(
                chat_id=id_,
                text=tpl.operator_new_ticket(
                    ticket_id=ticket.ticket_id,
                    username=msg.from_user.full_name,
                    dialog_type=ticket.dialog_type,
                    query=ticket.query
                ),
                reply_markup=kb_operator.get_accept_keyboard(ticket.ticket_id),
                parse_mode="html"
            )
            ticket.operator_notify_msgs[id_] = sent.message_id

        await msg.answer(tpl.USER_OPERATOR_WAIT, parse_mode='html')
