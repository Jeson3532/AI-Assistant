from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.frontend.bot.fsm.groups import Menus
from src.frontend.bot.templates import messages as msgs
from aiogram.filters import CommandStart

router = Router(name='Assistant Callback Router')


@router.callback_query(F.data == 'main_goto_assistant', Menus.START_MENU)
async def goto_assistant_chat(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Menus.ASSISTANT_CHAT)

    await cb.answer()
    await cb.message.answer(msgs.ASSISTANT_START_MESSAGE, parse_mode='html')


