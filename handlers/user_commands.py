from aiogram import Router
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
        text=f'<b>{message.from_user.first_name}</b>, здесь вся информация, как использовать бот\n'
             f'\n'
             f'/start - Начать все сначала(Твои данные не удалятся)\n'
             f'/menu - Вернуться в меню\n'
             f'/version - Смотри мою историю версий\n'
             f'/price - С помощью данной команды бот начинает мониторить цены, он делает это, <b>каждые 2 часа</b>\n'
             f'<i>Если хочешь чтобы я перестал это делать, введи любую команду</i>\n'
             f'\n'
             f'<b>Как пользоваться ботом?</b>'
             f'\n'
             f'1️⃣ В боте есть меню(Добавить товар, Удалить товар)\n'
             f'2️⃣ Нажимая на кнопку <b>ДОБАВИТЬ ТОВАР,</b> отправь ссылку товара и бот начнет ее анализировать\n'
             f'<i>Если ты отправлял такую же ссылку, то бот не даст тебе ее сохранить, пока ты ее не удалишь</i>\n'
             f'3️⃣ Нажимая на кнопку <b>УДАЛИТЬ ТОВАР,</b> выбери товар, который тебе не интересен и удали его\n'
             f'\n'
             f'🔅Как только ты добавил все товары, которые тебе нужно, нажми команду /price\n'
             # f'4️⃣ Нажимая на кнопку <b>ПОСМОТРЕТЬ ТОВАРЫ,</b> если забыл, какие у тебя товары анализируются.\n'
             f'\n'
             f'<i>Как правильно копировать ссылку на WB?</i>\n'
             f'1️⃣ Если в товаре нет размера, то копируй ссылку и отправляй в бот\n'
             f'2️⃣ Если в товаре есть размер, сначала выбери его, а потом копируй\n'
             f'\n'
             f'<b>За вопросами и предложениями, обращайся к моему создателю - </b>@masavnik'
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
        f'Скоро, все поменяется😉\n'
        f'\n'
        f'Я написан сыро - не ругайся на меня и на создателя, в скором времени он все исправит'
    )

