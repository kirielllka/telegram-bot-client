from time import sleep

from aiogram import F, Router, types, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.CallBackModels import PostCallBack
from bot.Request_result.requests_file import BaseResponces
from bot.text_file import *

from ..dicts import tokens
from ..States.StatesModel import Comment_state, Post_state

Post_router = Router()

delete_list_post = []
delete_list_profile = []
delete_comment_list = []
@Post_router.message(Command("start"))
async def starter(message: types.Message):
    await message.answer(hello_text)


@Post_router.message(Command("menu"))
async def menu(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Написать пост"),
        types.KeyboardButton(text="Посты"),
        types.KeyboardButton(text="Поиск поста"),
    )
    builder.row(types.KeyboardButton(text="Профиль"))
    await message.answer("Сейчас покажу!", reply_markup=builder.as_markup(resize_keyboard=True))


@Post_router.message(F.text.lower() == "посты")
async def al_posts_tg(message: types.Message, bot:Bot):
    builder = InlineKeyboardBuilder()
    delete_list_post.append(message.message_id)
    await bot.delete_messages(chat_id=message.chat.id, message_ids=delete_list_post)
    try:
        token = tokens[message.chat.id]
    except:
        token = None
    if not token:
        await message.answer("Сначала авторизуйтесь")
    else:
        posts = await BaseResponces.get_all_posts(token)
        print(posts)
        for post in posts:
            builder.row(
                types.InlineKeyboardButton(
                    text="Профиль автора",
                    callback_data=PostCallBack(foo="all_author", author_id=post["autor_info"]["id"], post_id=post["id"]).pack(),
                ),
                types.InlineKeyboardButton(
                    text="Комментарии",
                    callback_data=PostCallBack(foo="all_comment", author_id=post["autor_info"]["id"], post_id=post["id"]).pack(),
                ),
            )
            builder.row(
                types.InlineKeyboardButton(
                    text="Написать комментарий",
                    callback_data=PostCallBack(foo="for_comment", author_id=post["autor_info"]["id"], post_id=post["id"]).pack(),
                ),
                types.InlineKeyboardButton(
                    text="Удалить пост",
                    callback_data=PostCallBack(foo="delete", author_id=post["autor_info"]["id"], post_id=post["id"]).pack(),
                ),
            )
            text = (
                f"{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n"
                f"❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}"
            )

            msg = await message.answer(text=text, reply_markup=builder.as_markup())
            delete_list_post.append(msg.message_id)
            builder = InlineKeyboardBuilder()


@Post_router.callback_query(PostCallBack.filter(F.foo == "all_author"))
async def profile_author(query: CallbackQuery, callback_data: PostCallBack, bot:Bot):
    author_id = callback_data.author_id
    delete_list_profile.append(query.message.message_id)
    await bot.delete_messages(chat_id=query.message.chat.id, message_ids=delete_list_profile)
    try:

        token = tokens[query.message.chat.id]
    except:
        token = None
    if not token:
        await query.answer("Сначала авторизуйтесь")
    else:
        data = await BaseResponces.get_profile(author_id, token)
        print(data)
        print('sdsdsd')
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="Все посты пользователя",
                callback_data=PostCallBack(foo="post_by_user", author_id=author_id, post_id=1).pack(),
            )
        )
        text = f"{data['full_name']}\n{data['user_age']}\n{data['user_birth_date']}"
        msg = await query.message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))
        delete_list_profile.append(msg.message_id)

@Post_router.callback_query(PostCallBack.filter(F.foo == "all_comment"))
async def comments(query: CallbackQuery, callback_data: PostCallBack, bot:Bot):
    post_id = callback_data.post_id
    if len(delete_comment_list) > 0:
        await bot.delete_messages(chat_id=query.message.chat.id, message_ids=delete_comment_list)
    try:
        token = tokens[query.message.chat.id]
    except KeyError:
        token = None
    if not token:

        await query.answer("Сначала авторизуйтесь")
    else:
        data = await BaseResponces.comments_on_post(post_id, token)
        builder = InlineKeyboardBuilder()
        if len(data["results"]) == 0:
            await query.message.answer(text="Под данным постом нету комментариев")
        print(data)
        for post in data["results"]:
            builder.row(
                types.InlineKeyboardButton(
                    text="Профиль автора",
                    callback_data=PostCallBack(foo="all_author", author_id=post["user_info"]["id"], post_id=post["id"]).pack(),
                ),
            )
            text = (
                f"{post['content']}\nАвтор:{post['user_info']['username']}\n"
                f"❤️{post['like_count']}\nДата создания:{post['date_of_create'][:10]}"
            )
            msg = await query.message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))
            delete_comment_list.append(msg.message_id)


@Post_router.callback_query(PostCallBack.filter(F.foo == "for_comment"))
async def comment_create(query: CallbackQuery, callback_data: PostCallBack, state: FSMContext, bot:Bot):
    try:
        token = tokens[query.message.chat.id]
    except:
        token = None
    if not token:
        await query.answer("Сначала авторизуйтесь")
    else:
        post_id = callback_data.post_id
        await state.update_data(post=post_id)
        await state.set_state(Comment_state.content)
        await query.message.answer("Введите содержание комментария")


@Post_router.message(Comment_state.content)
async def comment_content(message: types.Message, state: FSMContext, bot:Bot):
    await state.update_data(content=message.text)
    data = await state.get_data()
    token = tokens[message.chat.id]
    req = await BaseResponces.create_comment(data=data, token=token, post_id=data["post"])
    print(req)
    msg = await message.answer("Ваш комментарий опубликован")
    sleep(10)
    await bot.delete_messages(chat_id=message.chat.id,message_ids=[msg.message_id,msg.message_id-1,msg.message_id-2,msg.message_id-3])
    await state.clear()


@Post_router.callback_query(PostCallBack.filter(F.foo == "post_by_user"))
async def posts_by_user(query: CallbackQuery, callback_data: PostCallBack, bot:Bot):
    author = callback_data.author_id
    builder = InlineKeyboardBuilder()
    if len(delete_list_post) > 0:
        await bot.delete_messages(chat_id=query.message.chat.id, message_ids=delete_list_post)
    try:
        token = tokens[query.message.chat.id]
    except:
        token = None
    if not token:
        await query.answer("Сначала авторизуйтесь")
    else:
        data = await BaseResponces.get_posts_by_user(author, token)
        for post in data:
            builder.row(
                types.InlineKeyboardButton(
                    text="Профиль автора",
                    callback_data=PostCallBack(foo="all_author", author_id=post["autor_info"]["id"],
                                               post_id=post["id"]).pack(),
                ),
                types.InlineKeyboardButton(
                    text="Комментарии",
                    callback_data=PostCallBack(foo="all_comment", author_id=post["autor_info"]["id"],
                                               post_id=post["id"]).pack(),
                ),
            )
            builder.row(
                types.InlineKeyboardButton(
                    text="Написать комментарий",
                    callback_data=PostCallBack(foo="for_comment", author_id=post["autor_info"]["id"],
                                               post_id=post["id"]).pack(),
                ),
                types.InlineKeyboardButton(
                    text="Удалить пост",
                    callback_data=PostCallBack(foo="delete", author_id=post["autor_info"]["id"],
                                               post_id=post["id"]).pack(),
                ),
            )
            text = (
                f"{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n"
                f"❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}"
            )

            msg = await query.message.answer(text=text, reply_markup=builder.as_markup())
            delete_list_post.append(msg.message_id)
            builder = InlineKeyboardBuilder()


@Post_router.message(F.text.lower() == "написать пост")
async def create_post(message: types.Message, state: FSMContext):
    try:

        token = tokens[message.chat.id]
    except:
        token = None
    if not token:
        await message.answer("Сначала авторизуйтесь")
    else:
        await state.set_state(Post_state.title)
        await message.answer("Введите заголовок поста")


@Post_router.message(Post_state.title)
async def post_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Post_state.content)
    await message.answer("Отлично!Введите содержание поста")


@Post_router.message(Post_state.content)
async def post_content(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    data = await state.get_data()
    data["categories"] = []
    token = tokens[message.chat.id]
    req = await BaseResponces.create_post(data=data, token=token)
    await message.answer("Отлично ваш пост создан")
    await state.clear()


@Post_router.callback_query(PostCallBack.filter(F.foo == "delete"))
async def delete_post(query: CallbackQuery, callback_data: PostCallBack):
    post_id = callback_data.post_id
    try:
        token = tokens[int(query.message.chat.id)]
    except:
        token = None
    if not token:
        await query.answer("Сначала авторизуйтесь")
    else:
        print(token)
        req = await BaseResponces.delete_post(post_id, token)
        if req == "Error":
            await query.answer("Вы не можете удалить чужой пост")
        else:
            await query.answer("Пост удален")
