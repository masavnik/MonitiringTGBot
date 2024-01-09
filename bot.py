import asyncio
from aiogram import Bot, Dispatcher
from handlers import user_commands


async def main():
    bot = Bot('6737553524:AAG5dFx-LKH26Suk8ePFbYw-Lz9mvPqJeus', parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(
        user_commands.router,

    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
