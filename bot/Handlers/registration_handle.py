
from aiogram.filters.command import Command

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram import F
from aiogram import Router

from ..Request_result.requests_file import BaseResponces

from ..States.StatesModel import Reg_state
import re

email = (r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

reg_router = Router()

@reg_router.message(Command('registration'))
async def registr_start(message:Message, state:FSMContext):
    await state.set_state(Reg_state.email)
    await message.answer(
        text='Введите свой email адресс'
    )

@reg_router.message(Reg_state.email)
async def registr_email(message:Message, state:FSMContext):
    try:
         if re.match(email, message.text):
             await state.update_data(email=message.text)
             await state.set_state(Reg_state.username)
             await message.answer(text='Теперь введите имя пользователя')
         else:
             await message.answer(
                 text='Почта введена некорректно'
             )
    except Exception:
       await message.answer('Ошибка в формате')

@reg_router.message(Reg_state.username)
async def register_name(message:Message, state:FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Отлично!Теперь введите пароль')
    await state.set_state(Reg_state.password)

@reg_router.message(Reg_state.password)
async def register_password(message:Message, state:FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    req = await BaseResponces.register(data)
    print(req)
    if req == 'Error':
        await message.answer(text='Что-то пошло не так, пройдите регистрацию заново')
    else:
        await message.answer(text='Регистрация прошла успешно!')
        await state.clear()


