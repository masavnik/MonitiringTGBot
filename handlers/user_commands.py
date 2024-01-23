from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.inline import main_kb, menu_link_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'Привет, <b>{message.from_user.first_name}</b>. '
        f'Я БОТ, который мониторит цены на маркетплейсе <b>WILDBERRIES.</b>\n'
        f'\n'
        f'P.S.\n'
        f'<b>Сейчас я нахожусь в стадии разработки, если будут вопросы,'
        f'напиши моему создателю</b> - @masavnik\n'
        f'\n'
        f'/help <b>- помощь в боте</b>',
        reply_markup=main_kb
    )


@router.message(Command('help'))
async def start(message: Message):
    await message.answer(
        text=f'<b>{message.from_user.first_name}</b>, это мои команды, которые ты можешь использовать\n'
             f'/start - Начать все сначала(Твои данные не удалятся)\n'
             f'/menu - Вернуться в меню\n'
             f'/version - Смотри мою историю версий\n'
             f'\n'
             f'<b>Как пользоваться ботом?</b>'
             f'\n'
             f'1️⃣ В боте есть меню(Добавить товар, Удалить товар, Посмотреть товары)\n'
             f'2️⃣ Нажимая на кнопку <b>ДОБАВИТЬ ТОВАР,</b> отправь ссылку товара и бот начнет ее анализировать\n'
             f'3️⃣ Нажимая на кнопку <b>УДАЛИТЬ ТОВАР,</b> выбери товар, которые тебе не интересен и удали его\n'
             f'4️⃣ Нажимая на кнопку <b>ПОСМОТРЕТЬ ТОВАРЫ,</b> если забыл какие у тебя товары анализируются.\n'
             f'\n'
             f'<b>За вопросом или предложению обращайся к моему создателю - </b>@masavnik'
    )


@router.message(Command('menu'))
async def start(message: Message):
    await message.answer(
        text=f'🟣<b>{message.from_user.first_name}, </b> выбери действие, которое хочешь сделать',
        reply_markup=menu_link_kb
    )


@router.message(Command('version'))
async def start(message: Message):
    await message.answer(
        f'<b>V1.0 - beta version</b>\n'
        f'Сейчась бот находится в beta версии. Все пользователи могут им пользоваться бесплатно.\n'
        f'Скоро, все поменяется😉'
    )
