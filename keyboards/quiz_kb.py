from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.dicts import *

bt_quiz_1 = InlineKeyboardButton(text="Числа 0-10", callback_data="10")
bt_quiz_2 = InlineKeyboardButton(text="Числа 0-20", callback_data="20")
bt_quiz_3 = InlineKeyboardButton(text="Числа 0-100", callback_data="100")
bt_quiz_4 = InlineKeyboardButton(
    text="Порядковые числительные", callback_data="ordinal"
)
bt_quiz_5 = InlineKeyboardButton(text="Личные местоимения", callback_data="pp")
kb_quiz = (
    InlineKeyboardMarkup(row_width=3)
    .row(bt_quiz_1, bt_quiz_2, bt_quiz_3)
    .row(bt_quiz_4)
    .row(bt_quiz_5)
)

kb_quiz_pp = InlineKeyboardMarkup(row_width=4)
row = 1

for key, value in PERSONAL_PRONOUNS_RU.items():
    if int(key[0]) == row:
        kb_quiz_pp.insert(InlineKeyboardButton(text=value, callback_data="pp_" + key))
    else:
        row += 1
        kb_quiz_pp.add(InlineKeyboardButton(text=value, callback_data="pp_" + key))
# kb_quiz_pp.add(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
