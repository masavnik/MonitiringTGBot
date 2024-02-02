import asyncio
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from parsing.parsing_wb import ParsingWB
from keyboards.inline import answer_link, menu_link_kb, exit_menu_kb
from sql.bot_sql import sql
from utils.states import AddProduct

router = Router()


@router.callback_query(F.data == 'add_product')
async def answer_link_user(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(add_product=callback.message.text)
    await state.set_state(AddProduct.data)
    await callback.message.answer(
        text='Отправь ссылку на товар и я буду ее анализировать\n'
             'После добавления ссылки введи команду - /price',
        reply_markup=exit_menu_kb
    )
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )


@router.message(F.text, AddProduct.data)
async def get_link_user(message: Message, bot: Bot, state: FSMContext):
    pars_wb = ParsingWB(message.text)
    all_data = pars_wb.get_data()
    photo = pars_wb.get_photo_product()

    if 'wildberries' not in message.text:
        # Переделать, чтобы находилось не только wildberies
        await message.answer(
            f'<b>{message.from_user.first_name}</b> отправь правильную ссылку с'
            f'маркетплейса <b>WILDBERRIES.</b>'
        )
    if message.text in sql.look_link(message.from_user.id):
        await message.answer(
            text=f'Товар под артикулом - <b>{all_data["Артикул"]}</b> уже есть в базе',
            reply_markup=exit_menu_kb
        )

    else:
        sent = await bot.send_message(message.chat.id, 'Получение данных товара🕐')
        animation = "🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛🕐"
        for i in range(10):
            await bot.edit_message_text(f"Получение данных товара{animation[i % len(animation)]}", message.chat.id,
                                        sent.message_id)
            await asyncio.sleep(0.1)
        await bot.delete_message(message.chat.id, sent.message_id)

        await state.update_data(
            link=message.text,
            name=all_data["Имя товара"],
            price=all_data["Цена"],
            count=all_data["Количество"],
            article=all_data['Артикул']
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



    await state.set_state(AddProduct.link)


@router.callback_query(F.data == 'save', AddProduct.link)
async def save_data(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(AddProduct.yes_add)
    data = await state.update_data(callback.message.text)
    link, name, price, count, article = data['link'], data['name'], data['price'], data['count'], data['article']

    sql.add_users(
        user_id=callback.from_user.id,
        article=article,
        product=name,
        price=price,
        count=count,
        link=link
    )

    await callback.answer('✅Ваша ссылка сохранена')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=f'🟣<b>{callback.from_user.first_name}, </b> выбери действие, которое хочешь сделать\n'
             f'Введи /price, чтобы я начал мониторить цену',
        reply_markup=menu_link_kb
    )


@router.callback_query(F.data == 'nosave', AddProduct.link)
async def save_data(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(AddProduct.no_add)
    await callback.message.answer(
        text=f'🟣<b>{callback.from_user.first_name}, </b> выбери действие, которое хочешь сделать\n',
        reply_markup=menu_link_kb
    )
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await state.clear()
