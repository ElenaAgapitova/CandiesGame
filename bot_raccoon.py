"""Модуль бота"""
from aiogram import types
import game
import random
import player
from asyncio import sleep
import text


async def bot_turn(message: types.Message):
    """Обработка хода бота"""
    await message.answer('Енот думает...🤔')
    await sleep(1)
    total = game.get_total()
    if game.level == 'с умным Енотом':
        if total <= game.update_step():
            take = total
        elif total % (game.update_step() + 1):
            take = total % (game.update_step() + 1)
        else:
            take = random.randint(1, game.update_step())
    else:
        if total <= game.update_step():
            take = total
        elif total <= ((game.update_step()) * 2 + 1) and total % (game.update_step() + 1):
            take = total % (game.update_step() + 1)
        else:
            take = random.randint(1, game.update_step())
    await message.answer(f'Енот берет {take} {text.declension_sweets(take)[0]}. '
                         f'На столе осталось {game.take_sweets(take)} '
                         f'{text.declension_sweets(game.get_total())[1]}.')

    if await game.check_win(message, 'bot'):
        return
    await player.player_turn(message)
