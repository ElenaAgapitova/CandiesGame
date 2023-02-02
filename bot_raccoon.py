"""Модуль бота"""
import game
import random
import player
from asyncio import sleep
import text
from create import bot


async def bot_turn(user_id):
    """Обработка хода бота"""
    await bot.send_message(chat_id=user_id, text='Енот думает...🤔')
    await sleep(1)
    total = game.get_total(user_id)
    if game.users[user_id]['level'] == 'с умным Енотом':
        if total <= game.users[user_id]['step']:
            take = total
        elif total % (game.users[user_id]['step'] + 1):
            take = total % (game.users[user_id]['step'] + 1)
        else:
            take = random.randint(1, game.users[user_id]['step'])
    else:
        if total <= game.users[user_id]['step']:
            take = total
        elif total <= ((game.users[user_id]['step']) * 2 + 1) \
                and total % (game.users[user_id]['step'] + 1):
            take = total % (game.users[user_id]['step'] + 1)
        else:
            take = random.randint(1, game.users[user_id]['step'])
    bot_msg = await bot.send_message(chat_id=user_id,
                                     text=f'Енот берет {take} {text.declension_sweets(take)[0]}. '
                                          f'На столе осталось {game.take_sweets(user_id, take)} '
                                          f'{text.declension_sweets(game.get_total(user_id))[1]}.')
    name = bot_msg.from_user.first_name
    if await game.check_win(user_id, name, 'bot'):
        return
    game.users[user_id]['turn'] = True
    await player.player_turn(user_id)
