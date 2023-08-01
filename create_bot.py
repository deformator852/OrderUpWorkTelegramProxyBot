from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = ""
# Token for BOT API

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
