from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from src.frontend.bot.storage import tickets
from src.frontend.bot.fsm.groups import Menus
from src.frontend.bot.utils.request import send_assistant_query
from src.frontend.bot.keyboards import operator as kb_operator
from src.frontend.bot.templates import messages as tpl
from src.frontend.bot.config import BotConfig

router = Router(name='Assistant Message Router')
BOT_CONFIG = BotConfig()


@router.message(Command("exit"), Menus.ASSISTANT_CHAT)
async def exit_chat(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Чат завершен.")


@router.message(Menus.ASSISTANT_CHAT, F.text.startswith("/"))
async def block_commands_user(msg: Message):
    await msg.answer("⚠️ Команды <b>недоступны</b> в режиме чата.\nДля выхода из чата используйте <b>/exit</b>", parse_mode='html')


@router.message(Menus.ASSISTANT_CHAT)
async def handle_message(msg: Message, state: FSMContext):
    # логика пересылки сообщений
    ticket = tickets.get_ticket_by_user(msg.from_user.id)
    if ticket and ticket.status == "in_progress":
        ticket.history.append({"role": "user", "text": msg.text})
        await msg.bot.send_message(
            ticket.operator_id,
            f"👤 Пользователь: {msg.text}"
        )
        return

    data = await state.get_data()
    history: list[dict] = data.get("history", [])

    # запрос
    response = await send_assistant_query(msg.text, history)
    answer = response['model_response']

    history.append({"role": "user", "text": msg.text})
    history.append({"role": "assistant", "text": answer})
    await state.update_data(history=history)

    await msg.answer(answer)

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
                    user_name=msg.from_user.full_name,
                    dialog_type=ticket.dialog_type,
                    query=ticket.query
                ),
                reply_markup=kb_operator.get_accept_keyboard(ticket.ticket_id),
                parse_mode="html"
            )
            ticket.operator_notify_msgs[id_] = sent.message_id

        await msg.answer(tpl.USER_OPERATOR_WAIT, parse_mode='html')
