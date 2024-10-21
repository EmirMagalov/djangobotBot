import asyncio
from private import user_private_router
from basket import basket_router
from fsm_add_adress import fsm_add_adress
from dotenv import load_dotenv
import os

load_dotenv()

from aiogram import Bot, Dispatcher



bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(fsm_add_adress)
dp.include_router(user_private_router)
dp.include_router(basket_router)

async def main():
    await dp.start_polling(bot)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("бот остановлен пользователем")