
from aiogram import  types
from aiogram.filters.command import Command

from aiogram.types import CallbackQuery
from aiogram import F

from aiogram import Router

from bot.CallBackModels import PostCallBack
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from bot.text_file import *
from bot.Request_result.requests_file import BaseResponces, token

from ..login_dicts import tokens

Post_router = Router()



@Post_router.message(Command('start'))
async def starter(message : types.Message):
    await message.answer(hello_text)


@Post_router.message(Command('menu'))
async def menu(message:types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Посты'),
        types.KeyboardButton(text='Поиск поста')
    )
    builder.row(
        types.KeyboardButton(text='Профиль')
    )
    await message.answer('Сейчас покажу!', reply_markup=builder.as_markup(resize_keyboard=True))


@Post_router.message(F.text.lower() == 'посты')
async def al_posts_tg(message:types.Message):
    builder = InlineKeyboardBuilder()
    try:
        token =tokens[message.chat.id]
    except:
        token = None
    if not token:
        await message.answer('Сначала авторизуйтесь')
    else:
        posts = await BaseResponces.get_all_posts(token)
        dict_post = {}
        for post in posts:
            builder.row(types.InlineKeyboardButton(text='Профиль автора', callback_data=PostCallBack(foo='all_author',author_id=post['autor_info']['id'],post_id=post['id']).pack()),
                types.InlineKeyboardButton(text='Комментарии', callback_data=PostCallBack(foo='all_comment',author_id=post['autor_info']['id'],post_id=post['id']).pack()),)
            text = (f'{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n'
                              f'❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}')

            await message.answer(text=text,reply_markup=builder.as_markup())
            builder = InlineKeyboardBuilder()



@Post_router.callback_query(PostCallBack.filter(F.foo == 'all_author'))
async def profile_author(query: CallbackQuery, callback_data:PostCallBack):
    author_id = callback_data.author_id
    try:
        token =tokens[query.chat.id]
    except:
        token = None
    if not token:
        await query.answer('Сначала авторизуйтесь')
    else:
        data = await BaseResponces.get_profile(author_id,token)
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(text='Все посты пользователя', callback_data=PostCallBack(foo='post_by_user',author_id=author_id,post_id=1).pack())
        )
        text = f'{data['full_name']}\n{data['age']}\n{data['user_birth_date']}'
        await query.message.answer(text=text,reply_markup=builder.as_markup(resize_keyboard=True))


@Post_router.callback_query(PostCallBack.filter(F.foo == 'all_comment'))
async def comments(query: CallbackQuery, callback_data:PostCallBack):
    post_id = callback_data.post_id
    try:
        token = tokens[query.chat.id]
    except:
        token = None
    if not token:
        await query.answer('Сначала авторизуйтесь')
    else:
        data = await BaseResponces.comments_on_post(post_id, token)
        builder = InlineKeyboardBuilder()
        if len(data['results']) == 0:
            await query.message.answer(text='Под данным постом нету комментариев')
        for post in data['results']:
            builder.row(
                types.InlineKeyboardButton(text='Профиль автора', callback_data=PostCallBack(foo='all_author',author_id=post['autor_info']['id'],post_id=post['id']).pack()),
            )
            text = (
                f'{post['title']}\n{post['content']}\nАвтор:{post['user_info']['username']}\n'
                f'❤️{post['like_count']}\nДата создания:{post['date_of_create'][:10]}')
            await query.message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))


@Post_router.callback_query(PostCallBack.filter(F.foo == 'post_by_user'))
async def posts_by_user(query: CallbackQuery, callback_data:PostCallBack):
    author = callback_data.author_id
    try:
        token =tokens[query.chat.id]
    except:
        token = None
    if not token:
        await query.answer('Сначала авторизуйтесь')
    else:
        data = await BaseResponces.get_posts_by_user(author,token)
        for post in data:
            await query.message.answer(
                f'{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}')
