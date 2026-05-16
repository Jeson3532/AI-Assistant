from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from src.frontend.bot.templates import messages as menu_template
from src.frontend.bot.keyboards import menu as menu_kb
from src.frontend.bot.fsm.groups import Menus
from src.frontend.bot.utils.request import send_assistant_query

router = Router(name='Assistant Message Router')


@router.message(Command("exit"), Menus.ASSISTANT_CHAT)
async def exit_chat(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Чат завершен.")


@router.message(Menus.ASSISTANT_CHAT)
async def start(msg: Message):
    response = await send_assistant_query(msg.text)
    await msg.answer(response['model_response'])
