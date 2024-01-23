from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from parsing.parsing_wb import ParsingWB
from keyboards.inline import answer_link, main_kb, menu_link_kb, exit_menu_kb
from sql.bot_sql import sql

router = Router()


@router.callback_query(F.data == 'wb')
async def answer_link_user(callback: CallbackQuery, bot: Bot):
    await callback.message.answer(
        f'🟣<b>{callback.from_user.first_name},</b> выбери действие, которое хочешь сделать\n',
        reply_markup=menu_link_kb
    )
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


@router.callback_query(F.data == 'exit_menu')
async def answer_link_user(callback: CallbackQuery, bot: Bot):
    await callback.message.answer(
        f'🟣<b>{callback.from_user.first_name},</b> выбери действие, которое хочешь сделать\n',
        reply_markup=menu_link_kb
    )
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)