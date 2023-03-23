from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("/help")
b2 = KeyboardButton("/quiz")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).insert(b2)
