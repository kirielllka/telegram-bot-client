from aiogram.fsm.state import State, StatesGroup


class Reg_state(StatesGroup):
    email = State()
    username = State()
    password = State()


class Login_state(StatesGroup):
    username = State()
    password = State()


class Post_state(StatesGroup):
    title = State()
    content = State()


class Comment_state(StatesGroup):
    post = State()
    content = State()

class Profile_state(StatesGroup):
    img = State()
    date_of_birth = State()
