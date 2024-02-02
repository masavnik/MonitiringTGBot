from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sql.bot_sql import sql

answer_link = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сохранить', callback_data='save'),
            InlineKeyboardButton(text='Не сохранять', callback_data='nosave')
        ]
    ]
)

menu_link_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✅Добавить товар', callback_data='add_product')
        ],
        # [
        #     InlineKeyboardButton(text='❇️Посмотреть товар', callback_data='look_product')
        # ],
        [
            InlineKeyboardButton(text='❎Удалить товар', callback_data='del_product')
        ]
    ]

)

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🟣wildberries🟣'.upper(), callback_data='wb'),
        ]
    ]
)


exit_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад в меню', callback_data='exit_menu'),
        ]
    ]
)


class LookCallbackFactory(CallbackData, prefix="req"):
    action: str


def get_keyboard_product(user_id):
    builder = InlineKeyboardBuilder()
    for i, y in enumerate(sql.look_product(user_id)):
        builder.button(
            text=f'{y[2]}', callback_data=LookCallbackFactory(action=f'{y[0]}')
        )
    builder.button(text='Назад в меню', callback_data='exit_menu')
    builder.adjust(1)
    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


class DelCallbackFactory(CallbackData, prefix="re"):
    action: str


def keyboard_product(user_id):
    builder = InlineKeyboardBuilder()
    for i, y in enumerate(sql.look_product(user_id)):
        builder.button(
            text=f'{y[2]}', callback_data=DelCallbackFactory(action=f'{y[0]}')
        )
    builder.button(text='Назад в меню', callback_data='exit_menu')
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
