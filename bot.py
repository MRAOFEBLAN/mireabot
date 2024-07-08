import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from database.models import async_main

TOKEN = '***'


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




