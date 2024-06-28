from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from dotenv.main import load_dotenv
import os

load_dotenv()

storage = MemoryStorage()
token_bot = os.environ["BOT_TOKEN"]
bot = Bot(token=token_bot, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=storage)
