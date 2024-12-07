import asyncio
import logging
from pyexpat.errors import messages

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os

from aiogram.types import CallbackQuery
from distlib.compat import text_type
from dotenv import load_dotenv
from aiogram import F
from poetry.core.masonry.builder import Builder

from bot.CallBackModels import PostCallBack
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from text_file import *
from bot.Request_result.requests_file import BaseResponces
from Registration import *
load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(str(os.getenv('TOKEN')))

dp = Dispatcher()




@dp.message(Command('start'))
async def starter(message : types.Message):
    await message.answer(hello_text)


@dp.message(Command('menu'))
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


@dp.message(F.text.lower() == 'посты')
async def al_posts_tg(message:types.Message):
    builder = InlineKeyboardBuilder()
    posts = await BaseResponces.get_all_posts()
    dict_post = {}
    for post in posts:
        builder.row(types.InlineKeyboardButton(text='Профиль автора', callback_data=PostCallBack(foo='all_author',author_id=post['autor_info']['id'],post_id=post['id']).pack()),
            types.InlineKeyboardButton(text='Комментарии', callback_data=PostCallBack(foo='all_comment',author_id=post['autor_info']['id'],post_id=post['id']).pack()),)
        text = (f'{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n'
                          f'❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}')

        await message.answer(text=text,reply_markup=builder.as_markup())
        builder = InlineKeyboardBuilder()



@dp.callback_query(PostCallBack.filter(F.foo == 'all_author'))
async def profile_author(query: CallbackQuery, callback_data:PostCallBack):
    author_id = callback_data.author_id
    data = await BaseResponces.get_profile(author_id)
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='Все посты пользователя', callback_data=PostCallBack(foo='post_by_user',author_id=author_id,post_id=None))
    )
    text = f'{data['full_name']}\n{data['age']}\n{data['user_birth_date']}'
    await query.message.answer(text=text,reply_markup=builder.as_markup(resize_keyboard=True))


@dp.callback_query(PostCallBack.filter(F.foo == 'all_comment'))
async def comments(query: CallbackQuery, callback_data:PostCallBack):
    post_id = callback_data.post_id
    data = await BaseResponces.comments_on_post(post_id)
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


@dp.callback_query(PostCallBack.filter(F.foo == 'post_by_user'))
async def posts_by_user(query: CallbackQuery, callback_data:PostCallBack):
    author = callback_data.author_id
    data = await BaseResponces.get_posts_by_user(author)
    for post in data:
        await query.message.answer(
            f'{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
