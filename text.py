"""Модуль текстовых сообщений и обработки текста"""

greetings = f', привет!\nСыграй со мной в конфетки🤗\n\n' \
            f'Сначала советую посмотреть в меню, что возможно в моей игре\n\t/menu'

menu = f', для этой игры используй следующие команды👇' \
       f'\n\n1. Старт => /start или /старт\n\n' \
       f'2. Начать игру => /new_game или /игра\n' \
       f'\n3. Правила игры => /rules или /правила\n\n' \
       f'4. Изменить уровень сложности => /level или /уровень\n' \
       f'По умолчанию я глупый Енот, попробуй забрать ' \
       f'все конфеты, если я буду умным🤯\n\n' \
       f'5. Изменить количество конфет => /set_total или /хочу' \
       f' и количество 🍬\n(по умолчанию 150 конфет)\n\n' \
       f'6. Изменить количество конфет за ход => /step или /шаг' \
       f' и количество 🍬\n(по умолчанию 28 конфет)\n\n ' \
       f'7. Все команды => /menu или /меню\n\n' \
       f'8. СТОП-ИГРА => /stop или /стоп'

rules = ', правила в игре простые.\n\n✅На столе лежат конфеты (по умолчанию 150). Мы играем, ' \
        'делая ход друг после друга. Первый ход определяется жеребьёвкой.\n\n✅За один ход ' \
        'можно забрать не менее 1 и не более чем определенное количество конфет (по умолчанию 28). ' \
        '\n\n✅Все конфеты достаются сделавшему последний ход, и он выигрывает.' \
        '\n\n✅Перед началом игры ты можешь выбрать уровень игры, максимальное количество конфет' \
        ' за ход и сколько всего конфет будешь делить со мной.' \
        '\n\n❌Во время игры данные изменения внести не получится!' \
        '\n\nНачать игру => /new_game'

answer1_for_set_total = 'Этой командой можно настроить количество конфет для игры.\n' \
                        'Введите /set_total или /хочу и количество конфет.'

answer2_for_set_total = 'Kоличество конфет можно изменить только ' \
                        'после окончания игры!'

answer_for_level = 'Изменить уровень можно только после окончания игры!'

stop_game = f'Ты больше не хочешь... Жаль😢'

answer1_for_set_step = 'Этой командой можно настроить максимальное количество конфет за ход.\n' \
                       'Введите /step или /шаг и количество конфет.'

answer2_for_set_step = 'Максимальное количество конфет за ход можно изменить только ' \
                       'после окончания игры!'


def declension_sweets(take: int):
    """Склонение слова 'конфета' в зависимости от количества"""
    size = len(str(take))
    last_dgt = take % 10
    second_last_dgt = take // 10 % 10
    if (size == 1 and take == 1) or \
            (size > 1 and last_dgt == 1 and second_last_dgt != 1):
        return 'конфету', 'конфета'
    if (size == 1 and take in [2, 3, 4]) or \
            (size > 1 and last_dgt in [2, 3, 4] and second_last_dgt != 1):
        return 'конфеты', 'конфеты'

    return 'конфет', 'конфет'
