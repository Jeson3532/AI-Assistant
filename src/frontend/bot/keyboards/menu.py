from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


def get_start_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="👤 Перейти в чат к ассистенту", callback_data="main_goto_assistant")],
        [InlineKeyboardButton(text="📈 Статистика", callback_data="main_statistic"),
         InlineKeyboardButton(text="🧩 О приложении", callback_data="main_util")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


def get_journal_keyboard(offset: int, total: int, limit: int = 5) -> InlineKeyboardMarkup | None:
    buttons = []
    if offset > 0:
        buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"journal_page_{offset - limit}"))
    if offset + limit < total:
        buttons.append(InlineKeyboardButton(text="Вперёд ▶️", callback_data=f"journal_page_{offset + limit}"))

    if not buttons:
        return None
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def back_to_main_menu():
    keyboard = [
        [InlineKeyboardButton(text="👤 Вернуться назад", callback_data="back_to_main_menu")],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup
