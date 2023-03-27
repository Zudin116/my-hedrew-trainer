from aiogram import types, Dispatcher
from num2words import num2words
from create_bot import bot
from keyboards import kb_client


HELLO_MESSAGE = "Hello! I'm Hebrew numbers bot!\n"
COMMAND_LIST = (
    "If you enter a number I will convert it to words.\n"
    "/help, /start - Show this message.\n"
    "/quiz - Little quiz about Hebrew numbers."
)


async def send_welcome(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        HELLO_MESSAGE + "\n" + COMMAND_LIST,
        reply_markup=kb_client,
    )


async def convert_to_words(message: types.Message):
    try:
        number = int(message.text)
    except ValueError:
        await message.answer("Enter a number")
        return
    await message.answer(num2words(number, lang="he"))


async def unknown_input(message: types.Message):
    await message.answer("Unknow comand")
    await message.answer(COMMAND_LIST)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start", "help"])
    dp.register_message_handler(
        convert_to_words, lambda message: message.text.isdigit()
    )
    dp.register_message_handler(unknown_input)
