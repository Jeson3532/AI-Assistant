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


@router.callback_query(F.data == 'main_goto_assistant', Menus.START_MENU)
async def goto_assistant_chat(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Menus.ASSISTANT_CHAT)

    await cb.answer()
    await cb.message.answer(msgs.ASSISTANT_START_MESSAGE, parse_mode='html')


@router.callback_query(F.data == 'main_statistic')
async def show_statistics(cb: CallbackQuery):
    await cb.answer()
    try:
        data = await get_analytics()
        await cb.message.answer(format_analytics(data), parse_mode='html')

        journal = await get_journal(limit=5, offset=0)
        markup = menu_kb.get_journal_keyboard(offset=0, total=journal["total"])
        await cb.message.answer(format_journal(journal), parse_mode='html', reply_markup=markup)
    except Exception as e:
        await cb.message.answer("Не удалось получить статистику. Попробуйте позже.")


@router.callback_query(F.data.startswith('journal_page_'))
async def paginate_journal(cb: CallbackQuery):
    await cb.answer()
    try:
        offset = int(cb.data.split("_")[-1])
        journal = await get_journal(limit=5, offset=offset)
        markup = menu_kb.get_journal_keyboard(offset=offset, total=journal["total"])
        await cb.message.edit_text(format_journal(journal), parse_mode='html', reply_markup=markup)
    except Exception:
        await cb.answer("Ошибка при загрузке страницы.", show_alert=True)
