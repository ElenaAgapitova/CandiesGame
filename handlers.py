"""Модуль взаимодействия с пользователем"""

from aiogram import types

import kb_inline
import keybutton
import game
import player
from create import dp, bot
import text


def default_decorator(func):
    async def wrapper(*args):
        user_id = args[0].from_user.id
        if user_id in game.users.keys():
            return await func(*args)
        else:
            await bot.send_message(chat_id=user_id,
                                   text=text.help_answer)
            game.users[user_id] = {'candy_total': game.SET_TOTAL, 'change_total': game.SET_TOTAL,
                                   'step': game.SET_STEP, 'turn': None,
                                   'level': game.LEVEL, 'game': False}
            return await func(*args)

    return wrapper


@dp.message_handler(commands=['start', 'старт'])
async def start(message: types.Message):
    """Приветствие пользователя. Старт"""
    name = message.from_user.first_name
    user_id = message.from_user.id
    img = open('images\\hello.jpg', 'rb')
    await bot.send_photo(user_id, img, caption=f'{name}{text.greetings}',
                         reply_markup=keybutton.kb_menu)
    user_id = message.from_user.id
    game.users[user_id] = {'candy_total': game.SET_TOTAL, 'change_total': game.SET_TOTAL,
                           'step': game.SET_STEP, 'turn': None,
                           'level': game.LEVEL, 'game': False}

    await player.log_user(message)


@dp.message_handler(commands=['rules', 'правила'])
async def game_rules(message: types.Message):
    """Правила игры"""
    name = message.from_user.first_name
    await message.answer(f'{name}{text.rules}')


@dp.message_handler(commands=['new_game', 'игра'])
@default_decorator
async def new_game(message: types.Message):
    """Запуск игры"""
    user_id = message.chat.id
    await game.start_game(user_id)


@dp.message_handler(commands=['set_total', 'хочу'])
@default_decorator
async def set_total(message: types.Message):
    """Изменить количество конфет"""
    user_id = message.from_user.id
    if not game.check_game(user_id):
        total = message.text.split()
        if len(total) > 1 and total[1].isdigit():
            game.update_total(user_id, int(total[1]))
            await message.answer(f'Kоличество конфет изменено на {total[1]}'
                                 f'\nНачать игру => /new_game')
        else:
            await message.answer(text.answer1_for_set_total)
    else:
        await message.answer(text.answer2_for_set_total)


@dp.message_handler(commands=['step', 'шаг'])
@default_decorator
async def set_step(message: types.Message):
    """Изменить количество конфет за ход"""
    user_id = message.from_user.id
    if not game.check_game(user_id):
        total = message.text.split()
        if len(total) > 1 and total[1].isdigit():
            await game.update_step(user_id, int(total[1]))
            await message.answer(f'Максимальное количество конфет за ход изменено на {total[1]}'
                                 f'\nНачать игру => /new_game')
        else:
            await message.answer(text.answer1_for_set_step)
    else:
        await message.answer(text.answer2_for_set_step)


@dp.message_handler(commands=['param'])
@default_decorator
async def show_params(message: types.Message):
    """Вывод параметров"""
    await game.show_param(message.from_user.id)


@dp.message_handler(commands=['difficult', 'сложность'])
@default_decorator
async def game_level(message: types.Message):
    """Изменить уровень сложности игры"""
    user_id = message.from_user.id
    if not game.users[user_id]['game']:
        await game.update_level(user_id)
        await message.answer(f'Ты будешь играть {game.users[user_id]["level"]}')
    else:
        await message.answer(text.answer_for_level)


@dp.message_handler(commands=['menu', 'меню'])
async def show_menu(message: types.Message):
    """Меню всех доступных команд"""
    name = message.from_user.first_name
    await message.answer(f'{name}{text.menu}')


@dp.message_handler(commands=['stop', 'стоп'])
@default_decorator
async def stop_game(message: types.Message):
    """Закончить игру"""
    user_id = message.from_user.id
    game.users[user_id]['game'] = False
    img = open('images\\stop_game.jpg', 'rb')
    await bot.send_photo(message.from_user.id, img, caption=f'{text.stop_game}')
    await message.answer(text='Когда передумаешь, жми👇', reply_markup=kb_inline.markup2)


@dp.callback_query_handler(text='up')
@default_decorator
async def wake_up(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await game.start_game(user_id)
    await callback.answer()


@dp.callback_query_handler(text=kb_inline.callback_list)
@default_decorator
async def get_result(callback: types.CallbackQuery):
    result = callback.data
    if result == 'yes':
        user_id = callback.from_user.id
        await game.start_game(user_id)
        await callback.answer()
    else:
        await callback.answer()
        img = open('images\\stop_game.jpg', 'rb')
        await bot.send_photo(callback.from_user.id, img, caption=f'{text.stop_game}')
        await callback.message.answer(text='Когда передумаешь, жми👇',
                                      reply_markup=kb_inline.markup2)


@dp.message_handler()
async def game_sweets(message: types.Message):
    """Обработка всех остальных сигналов от пользователя"""
    user_id = message.from_user.id
    name = message.from_user.first_name
    take = message.text
    if user_id in game.users.keys():
        if game.check_game(user_id):
            if game.users[user_id]['turn']:
                await player.player_game(user_id, take, name)
            else:
                await message.delete()
    else:
        await message.answer(f'{name}, я не понял, что ты хочешь🤨\n'
                             f'Попробуй найти что-то в меню => /menu')
