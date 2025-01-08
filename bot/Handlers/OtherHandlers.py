from time import sleep

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from ..OtherCode import logout
from ..dicts import tokens

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
        msg = await message.answer('Сейчас я вас забуду, вы вышли из аккаунта')
    delete_list.append(message.message_id)
    delete_list.append(msg.message_id)
    sleep(200)
    await bot.delete_messages(chat_id=message.chat.id, message_ids=delete_list )
