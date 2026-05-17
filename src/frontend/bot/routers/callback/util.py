from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.frontend.bot.fsm.groups import Menus
from src.frontend.bot.templates import messages as msgs
from src.frontend.bot.utils.request import get_analytics, get_journal
from src.frontend.bot.keyboards import menu as menu_kb
from src.frontend.bot.templates.messages import format_analytics, format_journal
from src.frontend.bot.utils.log import logger

router = Router(name='Assistant Callback Router')


@router.callback_query(F.data == 'main_util', Menus.START_MENU)
async def show_app_info(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await cb.message.answer(msgs.APP_INFO_MESSAGE, parse_mode='html', reply_markup=menu_kb.back_to_main_menu())
    await state.set_state(Menus.APP_INFO_MENU)


@router.callback_query(F.data == 'back_to_main_menu', Menus.APP_INFO_MENU)
async def show_app_info(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await cb.message.answer(msgs.START_MESSAGE, parse_mode='html', reply_markup=menu_kb.get_start_keyboard())
    await state.set_state(Menus.START_MENU)
