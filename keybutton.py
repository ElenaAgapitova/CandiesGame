from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)

btn_game = KeyboardButton('/игра')
btn_stop = KeyboardButton('/стоп')

kb_menu.add(btn_game, btn_stop)
