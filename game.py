"""Модуль игры"""
from asyncio import sleep

from create import bot
import kb_inline
import player
import bot_raccoon

SET_TOTAL = 150
SET_STEP = 28
LEVEL = 'с глупым Енотом'
users = {}


def default_decorator(func):
    async def wrapper(*args, **kwargs):
        user_id = args[0]
        if user_id in users.keys():
            return await func(*args, **kwargs)
        else:
            await bot.send_message(chat_id=user_id,
                                   text='Что-то пошло не так... Сейчас все поправим😇'
                                        '\nПопробуй еще разок.')
            users[user_id] = {'candy_total': SET_TOTAL, 'change_total': SET_TOTAL,
                              'step': SET_STEP, 'turn': None,
                              'level': LEVEL, 'game': False}
            print(users)
    return wrapper


# @default_decorator
async def update_step(user_id: int, value: int):
    """Изменить максимальное количество конфет за ход"""
    users[user_id]['step'] = value
    return users[user_id]['step']


# @default_decorator
def update_total(user_id: int, value: int) -> int:
    """Обновление количества конфет до начального заданного значения
    или по умолчанию"""
    users[user_id]['change_total'] = value
    return users[user_id]['change_total']


# @default_decorator
def get_total(user_id: int) -> int:
    """Получить текущее количество конфет"""
    return users[user_id]['candy_total']


# @default_decorator
def take_sweets(user_id: int, take: int):
    """Изменение количества конфет после хода игрока или бота"""
    users[user_id]['candy_total'] -= take
    return users[user_id]['candy_total']


# @default_decorator
def new_game(user_id: int):
    """Старт новой игры и обновление настроек"""
    if users[user_id]['game']:
        users[user_id]['game'] = False
    else:
        users[user_id]['game'] = True
    return users[user_id]['game']


# @default_decorator
def check_game(user_id: int):
    """Статус игры"""
    return users[user_id]['game']


# @default_decorator
async def check_win(user_id: int, name: str, whose_turn: str):
    """Проверка возможности выигрыша после хода игрока или бота"""
    img1 = open('images\\no.jpg', 'rb')
    img2 = open('images\\yes.jpg', 'rb')
    if users[user_id]['candy_total'] == 0:
        if whose_turn == 'player':
            users[user_id]['turn'] = False
            await bot.send_photo(user_id, img2, caption=f'Конфет на столе больше нет!'
                                                        f'\n{name}, ты забираешь '
                                                        f'всё.\nПоздравляю!🥇')
            await bot.send_message(chat_id=user_id, text='Сыграем еще?😉',
                                   reply_markup=kb_inline.markup)
        else:
            users[user_id]['turn'] = False
            await bot.send_photo(user_id, img1, caption=f'Конфет больше нет!\nВыиграл Енот!🎉\n')
            await bot.send_message(chat_id=user_id,
                                   text='Как насчет реванша?😎', reply_markup=kb_inline.markup)
        new_game(user_id)
        return True
    else:
        return False


# @default_decorator
async def update_level(user_id: int):
    """Изменить уровень игры"""
    if users[user_id]['level'] == 'с глупым Енотом':
        users[user_id]['level'] = 'с умным Енотом'
    else:
        users[user_id]['level'] = 'с глупым Енотом'


# @default_decorator
async def start_game(user_id: int):
    """Новая игра"""
    users[user_id]['candy_total'] = users[user_id]['change_total']
    users[user_id]['game'] = True
    if check_game(user_id):
        await show_param(user_id)
        await bot.send_message(chat_id=user_id,
                               text=f'Бросим кость🎲\n<b>Чет</b> - ходишь ты!\n<b>Нечет</b>- '
                                    f'ходит Енот!')
        dice_msg = await bot.send_dice(chat_id=user_id)
        await sleep(4)
        dice_value = dice_msg.dice.value
        users[user_id]['turn'] = dice_value % 2 == 0
        if not dice_value % 2:
            await player.player_turn(user_id)
        else:
            await bot.send_message(chat_id=user_id, text='Первый ходит Енот!')
            await bot_raccoon.bot_turn(user_id)


async def show_param(user_id: int):
    await bot.send_message(chat_id=user_id,
                           text=f'<b><u>Параметры игры:</u></b>\n'
                                f'\t▸ Конфеты на столе - {users[user_id]["candy_total"]}\n'
                                f'\t▸ Максимальное количество конфет за ход - '
                                f'{users[user_id]["step"]}\n'
                                f'\t▸ Играешь {users[user_id]["level"]}')
