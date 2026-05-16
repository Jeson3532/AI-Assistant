from src.frontend.bot.routers.callback.assistant import router as assistant_cb_router
from src.frontend.bot.routers.message.menu import router as base_menu_router
from src.frontend.bot.routers.message.assistant import router as assistant_router
from aiogram import Router

all_routers = [v for v in list(globals().values()) if isinstance(v, Router)]
