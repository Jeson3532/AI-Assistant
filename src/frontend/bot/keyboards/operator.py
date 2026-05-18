from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_accept_keyboard(ticket_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✋ Принять тикет", callback_data=f"accept_ticket:{ticket_id}")
    ]])


def get_ticket_taken_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="❌ Тикет уже принят", callback_data="ticket_taken")
    ]])


def get_save_to_kb_keyboard(ticket_id: int) -> InlineKeyboardMarkup:  # kb - knowledge base
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="💾 Сохранить в базу знаний", callback_data=f"save_kb_{ticket_id}")
    ]])
