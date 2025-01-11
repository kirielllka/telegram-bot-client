from time import sleep

from ..OtherCode import Token_add
from aiogram.filters.command import Command

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram import Router, Bot
from ..Request_result.requests_file import BaseResponces
from ..States.StatesModel import Login_state

from ..dicts import tokens

Login_router = Router()
delete_list = []
@Login_router.message(Command('login'))
async def login_start(message:Message, state:FSMContext):
    try:
        token = tokens[message.chat.id]
    except:
        token = None
    if token:
        msg = await message.answer('Вы уже авторизованы')
    else:
        await state.set_state(Login_state.username)
        msg = await message.answer(text='Введите имя пользователя чтобы я понял кто вы')
    delete_list.append(message.message_id)
    delete_list.append(msg.message_id)

@Login_router.message(Login_state.username)
async def login_name(message:Message, state:FSMContext):
    await state.update_data(username = message.text)
    msg = await message.answer(text=f'Имя {message.text} мне знакомо, точно ли это ты? Введи пароль')
    await state.set_state(Login_state.password)
    delete_list.append(message.message_id)
    delete_list.append(msg.message_id)

@Login_router.message(Login_state.password)
async def login_password(message:Message, state:FSMContext, bot:Bot):
    await state.update_data(password = message.text)
    data = await state.get_data()
    token = await BaseResponces.login(data)
    print(token)
    if token == 'Error':
        msg = await message.answer(text='Что-то пошло не так, проверьте корректность данных и начните авторизацию заново')
        await state.clear()
    else:
        await Token_add(token=token, user_id=message.chat.id)
        tokens[message.chat.id] = token
        msg = await message.answer(f'Как я мог тебя не узнать! Авторизация прошла успешно')
        await state.clear()
    delete_list.append(message.message_id)
    delete_list.append(msg.message_id)
    sleep(10)
    await bot.delete_messages(chat_id=message.chat.id,message_ids=delete_list, request_timeout=20)

