
from aiogram import  types
from aiogram.filters.command import Command
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message
from aiogram import F

from aiogram import Router
from certifi import contents

from bot.CallBackModels import PostCallBack
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from bot.text_file import *
from bot.Request_result.requests_file import BaseResponces

from ..States.StatesModel import Post_state,Comment_state

from ..login_dicts import tokens

Post_router = Router()



@Post_router.message(Command('start'))
async def starter(message : types.Message):
    await message.answer(hello_text)


@Post_router.message(Command('menu'))
async def menu(message:types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Написать пост'),
        types.KeyboardButton(text='Посты'),
        types.KeyboardButton(text='Поиск поста'),
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
            builder.row(types.InlineKeyboardButton(text='Профиль автора', callback_data=PostCallBack(foo='all_author',
                                                        author_id=post['autor_info']['id'],post_id=post['id']).pack()),

                types.InlineKeyboardButton(text='Комментарии', callback_data=PostCallBack(foo='all_comment',
                                                        author_id=post['autor_info']['id'],post_id=post['id']).pack()),

                types.InlineKeyboardButton(text='Написать комментарий', callback_data=PostCallBack(foo='for_comment',
                                                        author_id=post['autor_info']['id'],post_id=post['id']).pack())
                        ,)
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

            types.InlineKeyboardButton(text='Все посты пользователя', callback_data=PostCallBack(foo='post_by_user',
                                                author_id=author_id,post_id=1).pack())

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

                types.InlineKeyboardButton(text='Профиль автора', callback_data=PostCallBack(foo='all_author',
                                                author_id=post['autor_info']['id'],post_id=post['id']).pack()),

            )

            text = (
                f'{post['title']}\n{post['content']}\nАвтор:{post['user_info']['username']}\n'
                f'❤️{post['like_count']}\nДата создания:{post['date_of_create'][:10]}')
            await query.message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))

@Post_router.callback_query(PostCallBack.filter(F.foo == 'for_comment'))
async def comment_create(query: CallbackQuery, callback_data:PostCallBack, state:FSMContext):
    try:
        token = tokens[query.chat.id]
    except:
        token = None
    if not token:
        await query.answer('Сначала авторизуйтесь')
    else:
        post_id = callback_data.post_id
        await state.update_data(post=post_id)
        await state.set_state(Comment_state.content)
        await query.message.answer('Введите содержание комментария')

@Post_router.message(Comment_state.content)
async def comment_content(message:types.Message, state:FSMContext):
    await state.update_data(content = message.text)
    data = await state.get_data()
    token = tokens[message.chat.id]
    req = await BaseResponces.create_comment(data=data, token=token)
    print(req)
    await message.answer('Ваш комментарий опубликован')
    await state.clear()


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


@Post_router.message(F.text.lower() == 'написать пост')
async def create_post(message:types.Message, state:FSMContext):
    try:
        token =tokens[message.chat.id]
    except:
        token = None
    if not token:
        await message.answer('Сначала авторизуйтесь')
    else:
        await state.set_state(Post_state.title)
        await message.answer('Введите заголовок поста')


@Post_router.message(Post_state.title)
async def post_title(message:Message, state:FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Post_state.content)
    await message.answer('Отлично!Введите содержание поста')

@Post_router.message(Post_state.content)
async def post_content(message:types.Message, state:FSMContext):
    await state.update_data(content = message.text)
    data = await state.get_data()
    token = tokens[message.chat.id]
    req = await BaseResponces.create_post(data=data,token = token)
    print(req)
    await message.answer('Отлично ваш пост создан')
    await state.clear()




