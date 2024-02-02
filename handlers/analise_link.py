import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sql.bot_sql import sql
from parsing.parsing_wb import ParsingWB

router = Router()


@router.message(Command('price'))
async def analytics_price(message: Message):
    if not sql.look_product(message.from_user.id):
        await message.answer('У тебя нет товаров, которые можно анализировать\n'
                             'нажми /help и посмотри инструкцию')
    else:
        await message.answer(text='<b>Начинаю анализировать цены твоих товаров...</b>\n'
                                  '\n'
                                  'Следи за уведомлениями и не переключай команду.\n'
                                  'Чтобы отменить анализ, введи другую команду\n'
                                  'Все команды ты найдешь здесь - /help')

        while True:
            price_new = [
                ParsingWB(links[-1]).get_data()['Цена'] for links in sql.look_product(message.from_user.id)
            ]

            url = [i[-1] for i in sql.look_product(message.from_user.id)]
            article = [i[0] for i in sql.look_product(message.from_user.id)]
            price_product = [i[1] for i in sql.look_product(message.from_user.id)]
            name_product = [i[2] for i in sql.look_product(message.from_user.id)]

            for i_price_new, i_price, i_article, i_name, i_url in zip(price_new, price_product, article, name_product, url):
                if i_price_new < i_price:
                    button_link = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text=f'Купить товар', url=i_url),
                            ]
                        ]
                    )
                    await message.answer(
                        f'Товар: <b>{i_name}</b>\n'
                        f'Артикул: {i_article}\n'
                        f'\n'
                        f'📈<b>ЦЕНА СНИЗИЛАСЬ c {i_price} до {i_price_new}</b>\n'
                        f'Разница {i_price - i_price_new}₽\n',
                        reply_markup=button_link
                    )

                    sql.update(i_price_new, i_article)
            await asyncio.sleep(3600)
