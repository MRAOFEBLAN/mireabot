import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from database.models import async_main

TOKEN = '7176081427:AAGlj4W7tgIrU-9rRZOBWY3mFXgdj3EwkjE'

    


async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot=bot)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print('gg')






