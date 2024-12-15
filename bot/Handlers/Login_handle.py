
from aiogram.filters.command import Command

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram import F
from aiogram import Router

from ..Request_result.requests_file import BaseResponces
from ..States.StatesModel import Login_state

from ..login_dicts import tokens

Login_router = Router()

@Login_router.message(Command('login'))
async def login_start(message:Message, state:FSMContext):
    await state.set_state(Login_state.username)
    await message.answer(text='Введите имя пользователя чтобы я понял кто вы')

@Login_router.message(Login_state.username)
async def login_name(message:Message, state:FSMContext):
    await state.update_data(username = message.text)
    await message.answer(text=f'Имя {message.text} мне знакомо, точно ли это ты? Введи пароль')
    await state.set_state(Login_state.password)

@Login_router.message(Login_state.password)
async def login_password(message:Message, state:FSMContext):
    await state.update_data(password = message.text)
    data = await state.get_data()
    token = await BaseResponces.login(data)
    print(token)
    if token == 'Error':
        await message.answer(text='Что-то пошло не так, проверьте корректность данных и начните авторизацию заново')
        await state.clear()
    else:
        tokens[message.chat.id] = token
        await message.answer(f'Как я мог тебя не узнать! Авторизация прошла успешно')
        await state.clear()
