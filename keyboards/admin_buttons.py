from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

conn_cl = InlineKeyboardButton(text='Начать работу', callback_data='start_admin')
buttons_connect = InlineKeyboardMarkup(row_width=1)
buttons_connect.add(conn_cl)
