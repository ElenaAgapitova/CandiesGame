"""Создание телеграмм-бота"""
from aiogram import Bot, Dispatcher
import os

bot = Bot(os.getenv('TOKEN'), parse_mode='html')
dp = Dispatcher(bot)
