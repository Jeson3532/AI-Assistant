from aiogram import Dispatcher, Bot
from .config import BotConfig
from src.frontend.bot.routers import all_routers
import asyncio

CONFIG = BotConfig()


async def run():

    bot = Bot(token=CONFIG.token)
    dispatcher = Dispatcher()
    dispatcher.include_routers(*all_routers)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())
