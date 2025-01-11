import asyncio
import logging

from bot.Handlers.OtherHandlers import OtHandleRouter
from bot.Handlers.registration_handle import reg_router
from bot.Handlers.MAinHandles import Main_router
from bot.Handlers.Login_handle import Login_router
from bot.Handlers.admin_handles import admin_router



from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(str(os.getenv('TOKEN')))

dp = Dispatcher()




async def main():
    try:

        dp.include_routers(Main_router,reg_router,Login_router,admin_router,OtHandleRouter)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__ == '__main__':
    asyncio.run(main())
