from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton("/help")
b2 = KeyboardButton("/quiz")
b3 = KeyboardButton("/cancel")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1).insert(b2)

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel.add(b3)
