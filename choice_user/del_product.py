import asyncio
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from parsing.parsing_wb import ParsingWB
from keyboards.inline import answer_link, main_kb, menu_link_kb, exit_menu_kb, get_keyboard_group
from sql.bot_sql import sql
from utils.states import AddProduct

router = Router()


@router.callback_query(F.data == 'del_product')
async def answer_link_user(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = sql.look_product(callback.from_user.id)
    await callback.message.answer(
        text=f'Нажмите на продукт, который хотите удалить',
        reply_markup=get_keyboard_group(callback.from_user.id)
    )