from aiogram.fsm.state import State,StatesGroup


class Reg_state(StatesGroup):
    email = State()
    username = State()
    password = State()

class Login_state(StatesGroup):
    username = State()
    password = State()