from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.inline import main_kb, menu_link_kb
from sql.bot_sql import sql
from parsing.parsing_wb import ParsingWB

router = Router()


@router.message()
async def analitics_price(message: Message):
    link = [links[-1] for links in sql.look_product(message.from_user.id)]
    price_product = sql.look_product(message.from_user.id)[1]
    name_product = sql.look_product(message.from_user.id)[2]
    article = sql.look_product(message.from_user.id)[0]
    count_product = sql.look_product(message.from_user.id)[-2]
    while True:
        for i in link:
            pars = ParsingWB(i)
            price = pars.get_data()['Цена']
            if price < price_product[0]:
                await message.answer(
                    f'Цена товара {name_product} - {article} снижена до {price}'
                )
