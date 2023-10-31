import asyncio
import aiogram
import logging
from aiogram import types, Dispatcher
from typing import List, Union
from create_bot import dp, bot, clients_db
from keyboards.client_button import start_button
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup


logging.basicConfig(level=logging.ERROR, filename="py_client_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


class FSMAdmin(StatesGroup):
    message = State()


# Класс сделан для работы с коллажами фото, при получении 2 и выше фото
class AlbumMiddleware(BaseMiddleware):
    """Класс сделан для работы с коллажами фото, при получении 2 и выше фото.

    Класс решает проблему с перезапуском функции равным количеству полученных фото
    Пример использования:

    async def fnc(message: types.Message, album: List[types.Message]):

        if not message.media_group_id:
        ...
        else:
            media_group = types.MediaGroup()
            for obj in album:
                if obj.photo:
                    file_id = obj.photo[-1].file_id
                    caption = album[0].caption
                else:
                    file_id = obj[obj.content_type].file_id
                try:
                    media_group.attach({"media": file_id, "type": obj.content_type})
    """
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.05):
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            self.album_data[message.from_user.id] = [message]

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.from_user.id]
            return
        else:
            try:
                self.album_data[message.media_group_id].append(message)
                raise CancelHandler()
            except KeyError:
                self.album_data[message.media_group_id] = [message]
                await asyncio.sleep(self.latency)

                message.conf["is_last"] = True
                data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        if not message.media_group_id:
            if message.from_user.id and message.conf.get("is_last"):
                del self.album_data[message.from_user.id]
        else:
            if message.media_group_id and message.conf.get("is_last"):
                del self.album_data[message.media_group_id]


async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Привет пользователь!',
                           reply_markup=None)


async def back(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id='Мы вернулись назад!')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])

    dp.register_callback_query_handler(back, text='back_user', state="*")

    # dp.register_message_handler(connect, content_types=['text', 'photo'], state=FSMAdmin.message_admin)