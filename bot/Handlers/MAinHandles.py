import os
from datetime import datetime
from time import sleep

from PIL import Image

from aiogram import F, Router, types, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, KeyboardButton,FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.CallBackModels import PostCallBack
from bot.Request_result.requests_file import BaseResponces
from bot.text_file import *

from ..dicts import tokens
from ..States.StatesModel import Comment_state, Post_state, Profile_state, Post_red_state

Main_router = Router()

delete_list_post = []
delete_list_profile = []
delete_comment_list = []
@Main_router.message(Command("start"))
async def starter(message: types.Message):
    await message.answer(hello_text)


@Main_router.message(Command("menu"))
async def menu(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Написать пост"),
        types.KeyboardButton(text="Посты"),
        types.KeyboardButton(text="Поиск поста"),
    )
    builder.row(types.KeyboardButton(text="Профиль"))
    await message.answer("Сейчас покажу!", reply_markup=builder.as_markup(resize_keyboard=True))


@Main_router.message(F.text.lower() == "посты")
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
        if len(posts) ==0:
            msg = await message.answer('Постов нет')
            sleep(30)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
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
            builder.row(
                    types.InlineKeyboardButton(
                        text='Редактировать пост',
                        callback_data=PostCallBack(foo="re_post", author_id=post["autor_info"]["id"],
                                                   post_id=post["id"]).pack(),
                    ),
                )

            text = (
                f"{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n"
                f"❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}"
            )

            msg = await message.answer(text=text, reply_markup=builder.as_markup())
            delete_list_post.append(msg.message_id)
            builder = InlineKeyboardBuilder()


@Main_router.callback_query(PostCallBack.filter(F.foo == "all_author"))
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

        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="Все посты пользователя",
                callback_data=PostCallBack(foo="post_by_user", author_id=author_id, post_id=1).pack(),
            )
        )
        text = f"{data['full_name']}\n{data['user_age']}\n{data['user_birth_date']}"
        msg = await bot.send_photo(photo=photo,caption=text, reply_markup=builder.as_markup(resize_keyboard=True))
        delete_list_profile.append(msg.message_id)

@Main_router.callback_query(PostCallBack.filter(F.foo == "all_comment"))
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


@Main_router.callback_query(PostCallBack.filter(F.foo == "for_comment"))
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


@Main_router.message(Comment_state.content)
async def comment_content(message: types.Message, state: FSMContext, bot:Bot):
    await state.update_data(content=message.text)
    data = await state.get_data()
    token = tokens[message.chat.id]
    req = await BaseResponces.create_comment(data=data, token=token, post_id=data["post"])
    msg = await message.answer("Ваш комментарий опубликован")
    sleep(10)
    await bot.delete_messages(chat_id=message.chat.id,message_ids=[msg.message_id,msg.message_id-1,msg.message_id-2,msg.message_id-3])
    await state.clear()


@Main_router.callback_query(PostCallBack.filter(F.foo == "post_by_user"))
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
            builder.row(
            types.InlineKeyboardButton(
                text='Редактировать пост',
                callback_data=PostCallBack(foo="re_post", author_id=post["autor_info"]["id"],
                                               post_id=post["id"]).pack(),
                ),
            )

            text = (
                    f"{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n"
                    f"❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}")

            msg = await query.message.answer(text=text, reply_markup=builder.as_markup())
            delete_list_post.append(msg.message_id)
            builder = InlineKeyboardBuilder()


@Main_router.message(F.text.lower() == "написать пост")
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


@Main_router.message(Post_state.title)
async def post_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Post_state.content)
    await message.answer("Отлично!Введите содержание поста")


@Main_router.message(Post_state.content)
async def post_content(message: types.Message, state: FSMContext, bot:Bot):
    await state.update_data(content=message.text)
    data = await state.get_data()
    data["categories"] = []
    token = tokens[message.chat.id]
    req = await BaseResponces.create_post(data=data, token=token)
    await message.answer("Отлично ваш пост создан")
    await bot.delete_messages(chat_id=message.chat.id, message_ids=[message.chat.id,message.chat.id+1,message.chat.id-1,
                                                                    message.chat.id-2,message.chat.id-3,message.chat.id-4])
    await state.clear()


@Main_router.callback_query(PostCallBack.filter(F.foo == "delete"))
async def delete_post(query: CallbackQuery, callback_data: PostCallBack):
    post_id = callback_data.post_id
    try:
        token = tokens[int(query.message.chat.id)]
    except:
        token = None
    if not token:
        await query.answer("Сначала авторизуйтесь")
    else:
        req = await BaseResponces.delete_post(post_id, token)
        if req == "Error":
            await query.answer("Вы не можете удалить чужой пост")
        else:
            await query.answer("Пост удален")

@Main_router.message(F.text.lower() =='профиль')
async def profile(message:Message,bot:Bot):
    try:
        token = tokens[int(message.chat.id)]
    except:
        token = None
    if not token:
        await message.answer("Сначала авторизуйтесь")
    else:
        if len(delete_list_profile) > 0 :
            await bot.delete_messages(chat_id=message.chat.id, message_ids=delete_list_profile)
        user = await BaseResponces.user_me(token)
        user_id = user['id']
        photo = FSInputFile(f'/home/yanix/Desktop/Image_bot/{message.chat.id}.png')
        builder = InlineKeyboardBuilder()
        builder.row(
    types.InlineKeyboardButton(
                text="Все посты пользователя",
                callback_data=PostCallBack(foo="post_by_user", author_id=user_id, post_id=1).pack(),),
            types.InlineKeyboardButton(
                text="Редактировать профиль",
                callback_data=PostCallBack(foo="re_profile", author_id=user_id, post_id=1).pack(),),


        )
        data = await BaseResponces.get_profile(user_id, token)
        text = f"{data['full_name']}\n{data['user_age']}\n{data['user_birth_date']}"
        msg = await bot.send_photo(chat_id=message.chat.id,photo=photo,caption=text, reply_markup=builder.as_markup(resize_keyboard=True))
        delete_list_profile.append(msg.message_id)

@Main_router.callback_query(PostCallBack.filter(F.foo == "re_profile"))
async def red_profile(query: CallbackQuery, callback_data: PostCallBack, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    await state.update_data(id = callback_data.author_id)
    await state.set_state(Profile_state.img)
    builder.row(
        KeyboardButton(text='Оставить текущее')
    )
    await query.message.answer(text='Отправьте фото для своего профиля', reply_markup=builder.as_markup(resize_keyvoard=True))

@Main_router.message(Profile_state.img)
async def profile_photo(message, state:FSMContext, bot:Bot):
    if not message.photo:
        await message.answer(text='Хорошо, отправьте дату рождения в формате год-месяц-число')
        await state.set_state(Profile_state.date_of_birth)
    else:
        os.remove(f'/home/yanix/Desktop/Image_bot/{message.chat.id}.png')
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        destination_path = f'/home/yanix/Desktop/Image_bot/{message.chat.id}.png'  # Save to disk
        await bot.download_file(file_path, destination_path)
        img = Image.open(destination_path)
        path = f'/home/yanix/Desktop/Image_bot/{message.chat.id}.png'
        img.save(path)
        await state.update_data(img = path)
        await state.set_state(Profile_state.date_of_birth)
        await message.answer(text='Фото сохранено, введите дату рождения в формате год-месяц-число')

@Main_router.message(Profile_state.date_of_birth)
async def profile_date_of_birth(message, state:FSMContext, bot:Bot):
    token = tokens[message.chat.id]
    try:
        parts = message.text.split('-')
        year, month, day = int(parts[0]),int(parts[1]),int(parts[2])
        year_now = datetime.today().year
        if  not(100>(year_now-year)>0):
            await message.answer('Возраст может быть не больше 100 и не меньше 1, введите дату заново')
            await state.set_state(Profile_state.date_of_birth)
        elif year>year_now:
            await message.answer(f'Ваш год рождения не может быть позже {year_now}, введите дату заново')
            await state.set_state(Profile_state.date_of_birth)
        elif not(12>=month>=1):
            await message.answer('Неправильный месяц, введите дату заново')
            await state.set_state(Profile_state.date_of_birth)
        elif not(31>=day>=1):
            await message.answer('Неверное число, введите дату заново')
            await state.set_state(Profile_state.date_of_birth)
        else:
            await state.update_data(date = message.text)
            data =await state.get_data()
            try:
                datas = {
                    'image': data['img'],
                    'user_birth_date': data['date']
                }
            except:
                datas = {
                    'user_birth_date':data['date']
                }
            req = await BaseResponces.red_profile(token=token,user_id =data['id'],data=datas  )
            if req == 'Error':
                await message.answer('Что то пошло не так проверьте данные и начните заново')
                await state.clear()
            else:
                await message.answer('Профиль отредактирован')
                await state.clear()
                await bot.delete_messages(chat_id=message.chat.id, message_ids=[message.chat.id+1,message.chat.id,message.chat.id-1,message.chat.id-2])
    except ValueError:
        await message.answer('Неверный формат, введите дату заново')
        await state.set_state(Profile_state.date_of_birth)

@Main_router.callback_query(PostCallBack.filter(F.foo == "re_post"))
async def red_post(query: CallbackQuery, callback_data: PostCallBack, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    await state.update_data(post_id=callback_data.post_id)
    await state.set_state(Post_red_state.title)
    builder.row(
        KeyboardButton(text='Оставить текущее')
    )
    await query.message.answer('Напишите название поста', reply_markup=builder.as_markup(resize_keyvoard=True))

@Main_router.message(Post_red_state.title)
async def red_post_title(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Оставить текущее')
    )
    if message.text == 'Оставить текущее':
        await message.answer("Хорошо!Введите содержание поста", reply_markup=builder.as_markup(resize_keyvoard=True))
        await state.set_state(Post_state.content)

    else:
        await state.update_data(title=message.text)
        await state.set_state(Post_red_state.content)

        await message.answer("Отлично!Введите содержание поста", reply_markup=builder.as_markup(resize_keyvoard=True))


@Main_router.message(Post_red_state.content)
async def red_post_content(message: types.Message, state: FSMContext, bot:Bot):
        token = tokens[message.chat.id]
        if message.text != 'Оставить текущее':
            await state.update_data(content=message.text)
        data = await state.get_data()
        data["categories"] = []
        datas = {}
        for key in data.keys():
            if key != 'post_id':
                datas[key] = data[key]
        token = tokens[message.chat.id]
        req = await BaseResponces.red_post(token=token,user_id=data['post_id'], data=datas)
        await message.answer("Отлично ваш пост отредактирован")
        await bot.delete_messages(chat_id=message.chat.id, message_ids=[message.chat.id,message.chat.id+1,message.chat.id-1,
                                                                        message.chat.id-2,message.chat.id-3,message.chat.id-4])
        await state.clear()
