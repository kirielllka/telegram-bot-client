import asyncio
import logging

from bot.Handlers.Posts_handlers import Post_router

from aiogram import Bot, Dispatcher
import os

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(str(os.getenv('TOKEN')))

dp = Dispatcher()




async def main():
    try:
        dp.include_router(Post_router)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__ == '__main__':
    asyncio.run(main())
