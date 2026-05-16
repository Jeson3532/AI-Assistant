from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from src.frontend.bot.templates import messages as menu_template
from src.frontend.bot.keyboards import menu as menu_kb
from src.frontend.bot.fsm.groups import Menus

router = Router(name='Base Menu Router')


@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.set_state(Menus.START_MENU)
    await msg.answer(menu_template.START_MESSAGE, reply_markup=menu_kb.get_start_keyboard())
