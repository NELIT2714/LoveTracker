import os

import dotenv
from aiogram import Dispatcher, Bot
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis
from bot.functions import reformat_yaml

dotenv.load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
mongo = client[os.getenv("MONGO_DB")]
cache_redis = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)

from bot.callbacks import main_menu, create_pair
from bot.commands import start
