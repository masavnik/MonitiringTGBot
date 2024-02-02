from aiogram import Bot, Dispatcher
from choice_user import add_product, del_product, look_product, main_message
from handlers import analise_link, user_commands
from dotenv import load_dotenv
import os
import asyncio


async def main():
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(
        user_commands.router,
        look_product.router,
        analise_link.router,

        main_message.router,
        add_product.router,
        del_product.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
