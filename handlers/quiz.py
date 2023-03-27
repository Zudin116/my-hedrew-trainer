from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from num2words import num2words
import random

from keyboards import kb_quiz, kb_quiz_pp, kb_cancel, kb_client
from data import *


QUSTIONS = {"numbers": "Какое это число: ", "ordinal": "Какой это номер: "}
ANSWERS = {"numbers": "Это число ", "ordinal": "Это номер "}


class FSMQuiz(StatesGroup):
    qustion = State()
    right_answer = State()
    user_answer = State()
    attempts = State()
    game = State()


async def start_quiz(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args == "":
        await message.answer("Выберите вариант викторины:", reply_markup=kb_quiz)


async def numbers_quiz(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state()
    try:
        max = int(callback.data)
        game = "numbers"
        ordinal = False
    except ValueError:
        max = 10
        game = "ordinal"
        ordinal = True
    number = random.randrange(max)
    question = num2words(number, lang="he", ordinal=ordinal)
    await callback.message.answer(
        QUSTIONS[game] + question,
        reply_markup=kb_cancel,
    )
    await callback.answer()
    await state.set_state()
    async with state.proxy() as data:
        data["question"] = question
        data["right_answer"] = number
        data["attempts"] = 0
        data["game"] = game
    await FSMQuiz.user_answer.set()


async def check_numbers_quiz(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["attempts"] += 1
        if int(message.text) == data["right_answer"]:
            await message.answer("Правильный ответ!", reply_markup=kb_client)
            await state.finish()
        elif data["attempts"] < 3:
            await message.answer(
                "Неправильно. Попробуйте еще раз.\n"
                + QUSTIONS[data["game"]]
                + data["question"],
                reply_markup=kb_cancel,
            )
            await FSMQuiz.user_answer.set()
        else:
            await message.answer(
                "Неправильно. \n" + ANSWERS[data["game"]] + str(data["right_answer"]),
                reply_markup=kb_client,
            )
            await state.finish()


async def pp_quiz(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state()
    answer = random.choice(FORMS)
    question = PERSONAL_PRONOUNS_HE[answer]
    async with state.proxy() as data:
        data["question"] = question
        data["right_answer"] = answer
        data["attempts"] = 0
    await callback.message.answer(
        "Что здесь написано: " + question, reply_markup=kb_quiz_pp
    )
    await callback.answer()


async def check_pp_quiz(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["attempts"] += 1
        if callback.data.split("_")[1] == data["right_answer"]:
            await callback.message.answer("Правильно!", reply_markup=kb_client)
            await state.finish()
        elif data["attempts"] < 3:
            await callback.message.answer(
                "Неправильно. Попробуйте еще раз. Что здесь написано: "
                + data["question"],
                reply_markup=kb_quiz_pp,
            )
        else:
            await callback.message.answer(
                'Неправильно. Это "' + PERSONAL_PRONOUNS_RU[data["right_answer"]] + '"',
                reply_markup=kb_client,
            )
            await state.finish()
        await callback.answer()


async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Cancelled", reply_markup=kb_client)
        return
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer("Cancelled", reply_markup=kb_client)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, commands=["cancel"], state="*")
    dp.register_message_handler(start_quiz, commands=["quiz"], state=None)
    dp.register_message_handler(check_numbers_quiz, state=FSMQuiz.user_answer)
    dp.register_callback_query_handler(
        numbers_quiz,
        text=["10", "20", "100", "ordinal"],
    )
    dp.register_callback_query_handler(pp_quiz, text="pp")
    dp.register_callback_query_handler(check_pp_quiz, Text(startswith="pp_"))
    # dp.register_callback_query_handler(cancel_handler, text="cancel", state="*")
