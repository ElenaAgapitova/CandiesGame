from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

callback_list = ['yes', 'no']

buttons = [[InlineKeyboardButton(text='✅', callback_data='yes'),
            InlineKeyboardButton(text='❌', callback_data='no')]]

markup = InlineKeyboardMarkup(inline_keyboard=buttons)

btn = [[InlineKeyboardButton(text='Разбудить Енота😴', callback_data='up')]]
markup2 = InlineKeyboardMarkup(inline_keyboard=btn)
