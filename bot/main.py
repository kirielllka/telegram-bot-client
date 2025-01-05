import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from login_dicts import tokens

from bot.Handlers.admin_handles import admin_router
from bot.Handlers.Login_handle import Login_router
from bot.Handlers.Posts_handlers import Post_router
from bot.Handlers.registration_handle import reg_router

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(str(os.getenv("TOKEN")))

dp = Dispatcher()


async def main():
    try:

        print(tokens)
        dp.include_routers(Post_router, reg_router, Login_router, admin_router)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
