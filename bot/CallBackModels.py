from aiogram.filters.callback_data import CallbackData


class PostCallBack(CallbackData,prefix='post'):
    foo:str
    author_id : int
    post_id: int