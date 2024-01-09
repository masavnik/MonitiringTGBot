from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


answer_link = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сохранить', callback_data='save'),
            InlineKeyboardButton(text='Не сохранять', callback_data='nosave')
        ]
    ]
)
