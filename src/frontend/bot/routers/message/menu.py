from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from src.frontend.bot.templates import messages as tpl
from src.frontend.bot.keyboards import menu as menu_kb
from src.frontend.bot.fsm.groups import Menus
from aiogram.fsm.state import default_state

router = Router(name='Base Menu Router')


@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.set_state(Menus.START_MENU)
    await msg.answer(tpl.START_MESSAGE,
                     reply_markup=menu_kb.get_start_keyboard(),
                     parse_mode='html')


@router.message(StateFilter(default_state))
async def echo(msg: Message):
    await msg.answer("🤥 Ничего не понял! Для начала работы со мной используйте команду <b>/start</b>", parse_mode='html')
