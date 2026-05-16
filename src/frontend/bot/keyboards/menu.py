from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


def get_start_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="👤 Перейти в чат к ассистенту", callback_data="main_goto_assistant")],
        [InlineKeyboardButton(text="📈 Статистика", callback_data="main_statistic"),
         InlineKeyboardButton(text="🧩 О приложении", callback_data="main_util")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup
