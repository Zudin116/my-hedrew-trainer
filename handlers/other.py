from num2words import num2words
from aiogram import types, Dispatcher


async def convertor(message: types.Message):
    print(message)
    try:
        number = int(message.text)
    except:
        await message.answer("Enter a number")
    await message.answer(num2words(number, lang="he"))


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(convertor)
