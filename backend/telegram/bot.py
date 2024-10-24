import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
API_TOKEN = f'{os.getenv("TELEGRAM_API_TOKEN")}'


class NotyBot:
    bot = Bot(token=API_TOKEN)  # Инициализация бота
    dp = Dispatcher()  # Инициализация диспетчера

    def __init__(self):
        self.deploy_bot()

    async def deploy_bot(self):
        await self.dp.start_polling(self.bot)

    @dp.message(Command("start"))
    async def cmd_start(self, message: Message):
        await message.answer("Привет! Я бот, который поможет тебе получать уведомления из твоих любимых чатов!")

    @dp.message(Command("menu"))
    async def show_menu(self, message: Message):
        builder = ReplyKeyboardBuilder()

        builder.button(text="Подписки")
        builder.button(text="Аккаунт")
        builder.adjust(2)  # Количество кнопок в одном ряду

        await message.answer("Выберите опцию:", reply_markup=builder.as_markup())
