from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..OtherCode import logout
from ..login_dicts import tokens

OtHandleRouter = Router()

@OtHandleRouter.message(Command('logout'))
async def logout_handle(message:Message):
    try:
        token = tokens[message.chat.id]
    except:
        token = None
    if not token:
        await message.answer("Сначала авторизуйтесь")
    else:
        logout(message.chat.id)
        msg = await message.answer('Сейчас я вас забуду, вы вышли из аккаунта')