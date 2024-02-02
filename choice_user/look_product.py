import asyncio
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from parsing.parsing_wb import ParsingWB
from keyboards.inline import get_keyboard_product, LookCallbackFactory, menu_link_kb, exit_menu_kb
from sql.bot_sql import sql
from utils.states import LookProduct

router = Router()


@router.callback_query(F.data == 'look_product')
async def answer_link_user(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = sql.look_product_none_price(callback.from_user.id)
    await state.set_state(LookProduct.start_look)
    if not data:
        await callback.message.answer(text='В базе нет ваших продуктов\n'
                                           'Введи - /menu, чтобы вернуться в главное меню и добавить товар')
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id
        )
    else:
        await callback.message.answer(
            text=f'Выбери товар, который хочешь посмотреть',
            reply_markup=get_keyboard_product(callback.from_user.id)
        )
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id
        )


@router.callback_query(LookCallbackFactory.filter(), LookProduct.start_look)
async def callbacks_num_change(
        callback: CallbackQuery,
        callback_data: LookCallbackFactory,
        state: FSMContext,
        bot: Bot):
    pars = ParsingWB(f'https://www.wildberries.ru/catalog/{callback_data.action}/detail.aspx')
    all_data = pars.get_data()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        text=f'Твой товар <b>{all_data["Имя товара"]}</b>\n'
             f'\n'
             f'💎Артикул: <b>{all_data["Артикул"]}</b>\n'
             f'🔹Бренд: <b>{all_data["Бренд"]}</b>\n'
             f'⭐️Рейтинг: <b>{all_data["Рейтинг"]}</b>\n'
             f'📦Остаток на складе: <b>{all_data["Количество"]} шт.</b>\n'
             f'💰Цена: <b>{all_data["Цена"]} руб.</b>\n',
        reply_markup=exit_menu_kb
    )
    await state.clear()
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )