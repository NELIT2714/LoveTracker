import asyncio
import logging

from bot import bot, dp


async def run_bot():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
