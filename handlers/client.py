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
        "Hello!\nI'm EchoBot!\nPowered by aiogram.",
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
    await message.answer(num2words(number, lang="he"))
    await state.set_state()
    async with state.proxy() as data:
        data["number"] = number
    await FSMQuiz.answer.set()


async def check_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer"] = int(message.text)
        if data["number"] == data["answer"]:
            await message.answer("True")
            await state.finish()
        else:
            await message.answer("False")
            await FSMQuiz.answer.set()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start", "help"])
    dp.register_message_handler(quiz, commands=["quiz"], state=None)
    dp.register_message_handler(check_answer, state=FSMQuiz.answer)
    # dp.register_message_handler(convertor)
