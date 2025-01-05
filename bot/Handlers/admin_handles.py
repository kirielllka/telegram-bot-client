from aiogram import Router, types
from aiogram.filters.command import Command

from ..login_dicts import tokens

admin_router = Router()


@admin_router.message(Command("check"))
async def check_tokens(message: types.Message):
    await message.answer(text=f"{tokens}")
