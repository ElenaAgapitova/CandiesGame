"""Модуль игры"""
from aiogram import types

from create import bot
import kb_inline

set_total = 150
total = set_total
game = False
level = 'с глупым Енотом'
step = 28
set_step = 28
whose_turn = ''


def update_step():
    """Изменить максимальное количество конфет за ход"""
    global step
    global set_step
    step = set_step
    return step


def set_step_sweets(value: int):
    """Получить количество конфет за ход"""
    global set_step
    set_step = value
    return set_step


def update_total():
    """Обновление количества конфет до начального заданного значения
    или по умолчанию"""
    global total
    global set_total
    total = set_total


def set_total_sweets(value: int):
    """Изменение количества конфет"""
    global set_total
    set_total = value
    return set_total


def get_total():
    """Получить текущее количество конфет"""
    global total
    return total


def take_sweets(take: int):
    """Изменение количества конфет после хода игрока или бота"""
    global total
    total -= take
    return total


def new_game():
    """Старт новой игры и обновление настроек"""
    global game
    global total
    if game:
        game = False
    else:
        game = True
        total = set_total
    return game


def check_game():
    """Статус игры"""
    global game
    return game


async def check_win(message: types.Message, player: str):
    """Проверка возможности выигрыша после хода игрока или бота"""
    global whose_turn
    name = message.from_user.first_name
    user_id = message.from_user.id
    global game
    global level
    img1 = open('images\\no.jpg', 'rb')
    img2 = open('images\\yes.jpg', 'rb')
    if get_total() == 0:
        if player == 'player':
            whose_turn = False
            await bot.send_photo(user_id, img2, caption=f'Конфет на столе больше нет!'
                                                        f'\n{name}, ты забираешь '
                                                        f'всё.\nПоздравляю!🥇')
            await message.answer(text='Сыграем еще?😉', reply_markup=kb_inline.markup)
        else:
            whose_turn = False
            await bot.send_photo(user_id, img1, caption=f'Конфет больше нет!\nВыиграл Енот!🎉\n')
            await message.answer(text='Как насчет реванша?😎', reply_markup=kb_inline.markup)
        new_game()
        return True
    else:
        return False


def change_level():
    """Изменить уровень игры"""
    global level
    if level == 'с глупым Енотом':
        level = 'с умным Енотом'
    else:
        level = 'с глупым Енотом'
    return level
