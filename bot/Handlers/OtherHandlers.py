from time import sleep

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from bot.dicts.py import tokens
from bot.OtherCode.py import logout
OtHandleRouter = Router()
delete_list = []

@OtHandleRouter.message(Command('logout'))
async def logout_handle(message:Message, bot: Bot):
    try:
        token = tokens[message.chat.id]
    except:
        token = None
    if not token:
        msg = await message.answer("Сначала авторизуйтесь")
    else:
        await logout(message.chat.id)
        tokens.pop(f'{message.chat.id}')
        msg = await message.answer('Сейчас я вас забуду, вы вышли из аккаунта')
    delete_list.append(message.message_id)
    delete_list.append(msg.message_id)
    sleep(5)
    await bot.delete_messages(chat_id=message.chat.id, message_ids=delete_list )
