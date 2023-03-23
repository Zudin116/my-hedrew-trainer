from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from num2words import num2words
from create_bot import bot
from keyboards import kb_client
import random


class FSMQuiz(StatesGroup):
    number = State()
    answer = State()


async def send_welcome(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        """Hello!
        I'm Hedrew numbers bot!
        If you enter a number i will convert it to words(0-10000).
        
        /help, /start - Show this message.
        /quiz - litle quiz about hedrew numbers.
        """,
        reply_markup=kb_client,
    )


async def convertor(message: types.Message):
    print(message)
    try:
        number = int(message.text)
    except:
        await message.answer("Enter a number")
    await message.answer(num2words(number, lang="he"))


async def quiz(message: types.Message, state: FSMContext):
    number = random.randrange(10)

    await message.answer("What number is written here: " + num2words(number, lang="he"))
    await state.set_state()
    async with state.proxy() as data:
        data["number"] = number
    await FSMQuiz.answer.set()


async def check_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data["number"] == int(message.text):
            await message.answer("You're God damn right")
            await state.finish()
        else:
            await message.answer("Try again: " + num2words(data["number"], lang="he"))
            await FSMQuiz.answer.set()


async def convertor(message: types.Message):
    print(message)
    try:
        number = int(message.text)
    except:
        await message.answer("Enter a number")
    await message.answer(num2words(number, lang="he"))


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start", "help"])
    dp.register_message_handler(quiz, commands=["quiz"], state=None)
    dp.register_message_handler(check_answer, state=FSMQuiz.answer)
    dp.register_message_handler(convertor, lambda message: message.text.isdigit())
