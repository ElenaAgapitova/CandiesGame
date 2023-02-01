"""Модуль взаимодействия с пользователем"""

from aiogram import types

from asyncio import sleep

import kb_inline
import keybutton
import bot_raccoon
import game
import player
from create import dp, bot
import text
import datetime


@dp.message_handler(commands=['start', 'старт'])
async def start(message: types.Message):
    """Приветствие пользователя. Старт"""
    name = message.from_user.first_name
    user_id = message.from_user.id
    img = open('images\\hello.jpg', 'rb')
    await bot.send_photo(user_id, img, caption=f'{name}{text.greetings}',
                         reply_markup=keybutton.kb_menu)

    now = datetime.datetime.now()
    user = list()
    user.append(now.strftime("%d-%m-%Y %H:%M"))
    user.append(user_id)
    user.append(message.from_user.full_name)
    user.append(message.from_user.username)
    user = list(map(str, user))
    with open('users.txt', 'a', encoding='UTF-8') as data:
        data.write(' | '.join(user) + '\n')


@dp.message_handler(commands=['rules', 'правила'])
async def game_rules(message: types.Message):
    """Правила игры"""
    name = message.from_user.first_name
    await message.answer(f'{name}{text.rules}')


@dp.message_handler(commands=['new_game', 'игра'])
async def new_game(message: types.Message):
    """Запуск игры"""
    if not game.check_game():
        game.new_game()
    else:
        game.update_total()
    # name = message.from_user.first_name
    if game.check_game():
        await message.answer(f'На столе лежит {game.get_total()} '
                             f'{(text.declension_sweets(game.get_total()))[1]}.\n\n'
                             f'Бросим кость🎲\n<b>Чет</b> - ходишь ты!\n<b>Нечет</b>- ходит Енот!')
        dice_msg = await message.answer_dice()
        dice_value = dice_msg.dice.value
        await sleep(5)
        await message.answer(f'Выпало <b>{dice_value}</b>!')
        if not dice_value % 2:
            await player.player_turn(message)
        else:
            await message.answer(f'Первый ходит Енот!')
            await bot_raccoon.bot_turn(message)


@dp.message_handler(commands=['set_total', 'хочу'])
async def set_total(message: types.Message):
    """Изменить количество конфет"""
    if not game.check_game():
        total = message.text.split()
        if len(total) > 1 and total[1].isdigit():
            game.set_total_sweets(int(total[1]))
            await message.answer(f'Kоличество конфет изменено на {total[1]}'
                                 f'\nНачать игру => /new_game')
        else:
            await message.answer(text.answer1_for_set_total)
    else:
        await message.answer(text.answer2_for_set_total)


@dp.message_handler(commands=['step', 'шаг'])
async def set_step(message: types.Message):
    """Изменить количество конфет за ход"""
    if not game.check_game():
        total = message.text.split()
        if len(total) > 1 and total[1].isdigit():
            game.set_step_sweets(int(total[1]))
            await message.answer(f'Максимальное количество конфет за ход изменено на {total[1]}'
                                 f'\nНачать игру => /new_game')
        else:
            await message.answer(text.answer1_for_set_step)
    else:
        await message.answer(text.answer2_for_set_step)


@dp.message_handler(commands=['level', 'уровень'])
async def game_level(message: types.Message):
    """Изменить уровень сложности игры"""
    if not game.check_game():
        level = game.change_level()
        await message.answer(f'Ты будешь играть {level}')
    else:
        await message.answer(text.answer_for_level)


@dp.message_handler(commands=['menu', 'меню'])
async def show_menu(message: types.Message):
    """Меню всех доступных команд"""
    name = message.from_user.first_name
    await message.answer(f'{name}{text.menu}')


@dp.message_handler(commands=['stop', 'стоп'])
async def stop_game(message: types.Message):
    """Закончить игру"""
    game.new_game()
    img = open('images\\stopgame.jpg', 'rb')
    await bot.send_photo(message.from_user.id, img, caption=f'{text.stop_game}')
    await message.answer(text='Когда передумаешь, жми👇', reply_markup=kb_inline.markup2)


@dp.callback_query_handler(text='up')
async def wake_up(callback: types.CallbackQuery):
    await new_game(callback.message)


@dp.callback_query_handler(text=kb_inline.callback_list)
async def get_result(callback: types.CallbackQuery):
    result = callback.data
    if result == 'yes':
        await new_game(callback.message)
    else:
        img = open('images\\stopgame.jpg', 'rb')
        await bot.send_photo(callback.from_user.id, img, caption=f'{text.stop_game}')
        await callback.message.answer(text='Когда передумаешь, жми👇',
                                      reply_markup=kb_inline.markup2)


@dp.message_handler()
async def game_sweets(message: types.Message):
    """Обработка всех остальных сигналов от пользователя"""
    name = message.from_user.first_name
    take = message.text
    if game.check_game():
        await player.player_game(message, take, name)
    else:
        await message.answer(f'{name}{text.menu}')
