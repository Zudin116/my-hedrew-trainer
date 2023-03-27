from aiogram import executor

from create_bot import dp
from handlers import client, quiz


async def on_startup(_):
    print("Bot started")


quiz.register_handlers_client(dp)
client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
