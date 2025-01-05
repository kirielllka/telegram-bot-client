import asyncio
import logging
import os

from aiogram import  Dispatcher,Bot
from dotenv import load_dotenv
from login_dicts import tokens

from bot.Handlers.admin_handles import admin_router
from bot.Handlers.Login_handle import Login_router
from bot.Handlers.Posts_handlers import Post_router
from bot.Handlers.registration_handle import reg_router
from bot.Handlers.OtherHandlers import OtHandleRouter

from aiogram.types import BotCommand

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot_ex = Bot(str(os.getenv("TOKEN")))

dp = Dispatcher()

command_list = [
    BotCommand(command='start', description='Запустить бота'),
    BotCommand(command='registration', description='Начать регистрацию'),
    BotCommand(command='login', description='Начать авторизацию'),
    BotCommand(command='logout', description='Выйти из аккаунта'),

]


async def main():
    try:
        await bot.set_my_commands(commands=command_list)
        print(tokens)
        dp.include_routers(Post_router, reg_router, Login_router, admin_router,OtHandleRouter )
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
