from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def get_callback_btns(bt: dict[str, str],size_1=1,size_2=1):
    welcome = InlineKeyboardBuilder()
    for text, data in bt.items():
        welcome.add(

            InlineKeyboardButton(text=text, callback_data=data)
        )
    return welcome.adjust(size_1,size_2).as_markup()