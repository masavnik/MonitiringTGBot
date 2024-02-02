import asyncio
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from parsing.parsing_wb import ParsingWB
from keyboards.inline import keyboard_product, DelCallbackFactory, menu_link_kb
from sql.bot_sql import sql
from utils.states import DelProduct

router = Router()


@router.callback_query(F.data == 'del_product')
async def answer_link_user(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(DelProduct.start_del)
    data = sql.look_product(callback.from_user.id)
    if not data:
        await callback.message.answer(text='В базе нет ваших продуктов\n'
                                           'Нажми - /menu, чтобы вернуться в меню')
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id
        )
    else:

        await callback.message.answer(
            text=f'Нажмите на продукт, который хотите удалить',
            reply_markup=keyboard_product(callback.from_user.id)
        )
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id
        )


@router.callback_query(DelCallbackFactory.filter(), DelProduct.start_del)
async def callbacks_num_change(
        callback: CallbackQuery,
        callback_data: DelCallbackFactory,
        state: FSMContext,
        bot: Bot):
    sql.del_product(callback_data.action)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        text=f'<b>Товар: артикул - {callback_data.action} удален</b>',
    )
    await callback.message.answer(
        text=f'🟣Выбери действие, которое хочешь сделать',
        reply_markup=menu_link_kb
    )
    await state.clear()
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )


