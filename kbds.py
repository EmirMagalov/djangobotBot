from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


cancel=ReplyKeyboardBuilder()
cancel.add(
    KeyboardButton(text="Отмена"),

)
cancel.adjust(1)


remove_kb=ReplyKeyboardRemove()