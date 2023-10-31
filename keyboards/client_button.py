from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

button_start = InlineKeyboardButton(text='Начать работу', callback_data='start_button')
start_button = InlineKeyboardMarkup(row_width=1)
start_button.add(button_start)


