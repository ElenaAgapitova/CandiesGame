"""Модуль игрока"""
from aiogram import types
import game
import bot_raccoon
import text
import datetime
from create import bot


async def log_user(message: types.Message):
    """Запись пользователя в файл"""
    now = datetime.datetime.now()
    user = list()
    user.append(now.strftime("%d-%m-%Y %H:%M"))
    user.append('id: ' + str(message.from_user.id))
    user.append('full_name: ' + str(message.from_user.full_name))
    user.append('username: ' + str(message.from_user.username))
    with open('users.txt', 'a', encoding='UTF-8') as data:
        data.write(' | '.join(user) + '\n')


async def player_turn(user_id: int):
    """Ход игрока"""
    await bot.send_message(chat_id=user_id, text='Твой ход! Сколько конфет возьмешь?')


async def player_game(user_id: int, take: str, name: str):
    """Обработка хода игрока"""
    if take.isdigit():
        take = int(take)
        if (game.get_total(user_id) - take) < 0:
            await bot.send_message(chat_id=user_id,
                                   text=f'{name}, хочет взять - {take} {text.declension_sweets(take)[0]},'
                                        f' но на столе всего {game.get_total(user_id)}.\n'
                                        f'Возьми поменьше, не жадничай😃')
        elif take <= 0 or take > game.users[user_id]['step']:
            await bot.send_message(chat_id=user_id,
                                   text=f'{name}, можно брать не менее 1 и '
                                        f'не более {game.users[user_id]["step"]}👆')
        elif 1 <= take <= game.users[user_id]["step"]:
            game.users[user_id]['turn'] = False
            game.take_sweets(user_id, take)
            if await game.check_win(user_id, name, 'player'):
                return
            if take <= 5:
                await bot.send_message(chat_id=user_id,
                                       text=f'{name} берет всего {take} '
                                            f'{text.declension_sweets(take)[0]}.'
                                            f'\nЧто так мало? Бери больше,'
                                            f' не скромничай😋\n\n'
                                            f'На столе осталось {game.get_total(user_id)} '
                                            f'{text.declension_sweets(game.get_total(user_id))[1]}. '
                                            f'Ходит Енот!')
                await bot_raccoon.bot_turn(user_id)
            elif take >= game.users[user_id]["step"] - 5:
                await bot.send_message(chat_id=user_id,
                                       text=f'{name} берет аж {take} {text.declension_sweets(take)[0]}.'
                                            f'\nМного сладкого вредно😏\n'
                                            f'\nНа столе осталось {game.get_total(user_id)} '
                                            f'{text.declension_sweets(game.get_total(user_id))[1]}. '
                                            f'Ходит Енот!')
                await bot_raccoon.bot_turn(user_id)
            else:
                await bot.send_message(chat_id=user_id,
                                       text=f'{name} берет {take} {text.declension_sweets(take)[0]}.'
                                            f'\nНа столе осталось {game.get_total(user_id)} '
                                            f'{text.declension_sweets(game.get_total(user_id))[1]}. '
                                            f'Ходит Енот!')
                await bot_raccoon.bot_turn(user_id)
    else:
        await bot.send_message(chat_id=user_id,
                               text=f'Что-то тут не то! Вводи число🤦')
