from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message, CallbackQuery
from parsing_wb import ParsingWB
from keyboards.inline import answer_link
from utils.states import LinkUser
from bot_sql import sql

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(LinkUser.link)
    await message.answer(f'Привет, <b>{message.from_user.first_name}</b>. '
                         f'Я БОТ, который мониторит цены на маркетплейсе <b>WILDBERRIES.</b>\n'
                         f'Отправь мне ссылку и начну анализировать цену товара\n'
                         f'\n'
                         f'P.S.\n'
                         f'<b>Сейчас я нахожусь в стадии разработки, если будут вопросы,'
                         f'напиши моему создателю</b> - @masavnik')


@router.message(F.text, LinkUser.link)
async def get_link_user(message: Message, bot: Bot, state: FSMContext):
    if 'wildberries' not in message.text:
        # Переделать, чтобы находилось не только wildberies
        await message.answer(
            f'<b>{message.from_user.first_name}</b> отправь правильную ссылку с'
            f'маркетплейса <b>WILDBERRIES.</b>'
        )
    else:
        pars_wb = ParsingWB(message.text)
        all_data = pars_wb.get_data()
        photo = pars_wb.get_photo_product()
        await state.update_data(
            link=message.text,
            name=all_data["Имя товара"],
            price=all_data["Цена"],
            count=all_data["Количество"]
        )
        await bot.send_photo(
            message.chat.id,
            photo=photo,
            caption=f'💎Артикул: <b>{all_data["Артикул"]}</b>\n'
                    f'🔹Бренд: <b>{all_data["Бренд"]}</b>\n'
                    f'🟣Имя товара: <b>{all_data["Имя товара"]}</b>\n'
                    f'⭐️Рейтинг: <b>{all_data["Рейтинг"]}</b>\n'
                    f'📦Остаток на складе: <b>{all_data["Количество"]} шт.</b>\n'
                    f'💰Цена: <b>{all_data["Цена"]} руб.</b>\n',
            reply_markup=answer_link
        )

        await state.set_state(LinkUser.data)


@router.callback_query(F.data == 'save', LinkUser.data)
async def save_data(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data(callback.message.text)
    link, name, price, count = data['link'], data['name'], data['price'], data['count']
    sql.add_users(
        user_id=callback.from_user.id,
        product=name,
        price=price,
        count=count,
        link=link
    )
    await callback.message.answer('Ваша ссылка сохранена')


@router.callback_query(F.data == 'nosave')
async def save_data(callback: CallbackQuery):
    await callback.message.answer('Ок')
