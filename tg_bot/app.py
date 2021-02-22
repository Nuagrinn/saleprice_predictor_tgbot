from aiogram import Bot, Dispatcher, types
from aiogram import executor
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


async def on_shutdown(dp):
    await bot.close()
    await storage.close()

if __name__ == '__main__':
    from prediction_handlers import dp
    executor.start_polling(dp, on_shutdown=on_shutdown)
