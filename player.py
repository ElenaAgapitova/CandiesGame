"""Модуль игрока"""
from aiogram import types
import game
import bot_raccoon
import text


async def player_turn(message: types.Message):
    """Ход игрока"""
    name = message.from_user.full_name
    await message.answer(f'{name}, твой ход! Сколько конфет возьмешь?')


async def player_game(message: types.Message, take: str, name: str):
    """Обработка хода игрока"""
    if take.isdigit():
        take = int(take)
        if (game.get_total() - take) < 0:
            await message.answer(f'{name}, хочет взять - {take} {text.declension_sweets(take)[0]},'
                                 f' но на столе всего {game.get_total()}.\n'
                                 f'Возьми поменьше, не жадничай😃')
        elif take <= 0 or take > game.update_step():
            await message.answer(f'{name}, можно брать не менее 1 и '
                                 f'не более {game.update_step()}👆')
        elif 1 <= take <= game.update_step():
            game.take_sweets(take)
            if await game.check_win(message, 'player'):
                return
            if take <= 5:
                await message.answer(f'{name} берет всего {take} '
                                     f'{text.declension_sweets(take)[0]}.'
                                     f'\nЧто так мало? Бери больше,'
                                     f' не скромничай😋\n\n'
                                     f'На столе осталось {game.get_total()} '
                                     f'{text.declension_sweets(game.get_total())[1]}. '
                                     f'Ходит Енот!')
                await bot_raccoon.bot_turn(message)
            elif take >= game.update_step() - 5:
                await message.answer(f'{name} берет аж {take} {text.declension_sweets(take)[0]}.'
                                     f'\nМного сладкого вредно😏\n'
                                     f'\nНа столе осталось {game.get_total()} '
                                     f'{text.declension_sweets(game.get_total())[1]}. Ходит Енот!')
                await bot_raccoon.bot_turn(message)
            else:
                await message.answer(f'{name} берет {take} {text.declension_sweets(take)[0]}.'
                                     f'\nНа столе осталось {game.get_total()} '
                                     f'{text.declension_sweets(game.get_total())[1]}. Ходит Енот!')
                await bot_raccoon.bot_turn(message)
    else:
        await message.answer(f'Что-то тут не то! Вводи число🤦')
