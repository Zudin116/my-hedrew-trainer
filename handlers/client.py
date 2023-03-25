from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from num2words import num2words
from create_bot import bot
from keyboards import kb_client, kb_cancel
import random


class FSMQuiz(StatesGroup):
    number = State()
    answer = State()


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


async def start_quiz(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args == "":
        max = 10
    else:
        max = int(args)
    number = random.randrange(max)
    await message.answer(
        f"What number is written here: {num2words(number, lang='he')}",
        reply_markup=kb_cancel,
    )
    await state.set_state()
    async with state.proxy() as data:
        data["number"] = number
    await FSMQuiz.answer.set()


async def check_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data["number"] == int(message.text):
            await message.answer("You're God damn right", reply_markup=kb_client)
            await state.finish()
        else:
            await message.answer(f"Try again: {num2words(data['number'], lang='he')}")
            await FSMQuiz.answer.set()


async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer("Cancelled", reply_markup=kb_client)


async def unknown_input(message: types.Message):
    await message.answer("Unknow comand")
    await message.answer(COMMAND_LIST)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start", "help"])
    dp.register_message_handler(start_quiz, commands=["quiz"], state=None)
    dp.register_message_handler(cancel_handler, commands=["cancel"], state="*")
    dp.register_message_handler(check_answer, state=FSMQuiz.answer)
    dp.register_message_handler(
        convert_to_words, lambda message: message.text.isdigit()
    )
    dp.register_message_handler(unknown_input)
