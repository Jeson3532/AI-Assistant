from aiogram.fsm.state import State, StatesGroup


class Menus(StatesGroup):
    START_MENU = State()
    ASSISTANT_CHAT = State()


class Operator(StatesGroup):
    HANDLE_TICKET = State()
