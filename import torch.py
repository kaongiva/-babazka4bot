import telebot
import random
from telebot import types

# Токен вашего бота, который вы получили у @BotFather
TOKEN = ''

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения игровых сессий крестиков-ноликов
games = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для игр. Вот список доступных игр: \n\n"
                                      "/help - Помощь\n"
                                      "Чтобы запустить бота, используйте /start")

# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Если возникла проблема, вот список команд, которые у меня есть: \n\n"
                                      "/tic_tac_toe - игра в крестики-нолики\n"
                                      "/guess_who - угадай персонажа\n"
                                      "/help - вызов этого окна\n"
                                      "/conf - Конф. ботa\n")

# Команда /conf
@bot.message_handler(commands=['conf'])
def conf(message):
    bot.send_message(message.chat.id, "Создатель бота: @mR_nekt0o. Подробная информация о боте: https://telegra.ph/Komandy-bota-04-25")


# Команда /tic_tac_toe
@bot.message_handler(commands=['tic_tac_toe'])
def tic_tac_toe(message):
    chat_id = message.chat.id
    if chat_id in games:
        bot.send_message(chat_id, "Игра уже идет!")
    else:
        markup = generate_tic_tac_toe_markup(chat_id)
        msg = bot.send_message(chat_id, "Игра началась! Для хода выберите одно из полей на игровом поле ниже:", reply_markup=markup)
        games[chat_id] = {
            'board': [' ']*9,
            'turn': 'X',
            'message_id': msg.message_id
        }

# Генерация разметки для игры в крестики-нолики
def generate_tic_tac_toe_markup(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i in range(9):
        buttons.append(types.InlineKeyboardButton(" ", callback_data=str(i)))
    markup.add(*buttons)
    return markup

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    if chat_id in games:
        position = int(call.data)
        play_tic_tac_toe(chat_id, position)
        bot.answer_callback_query(call.id)
    else:
        bot.send_message(chat_id, "Игра не начата. Введите /tic_tac_toe, чтобы начать игру.")

# Логика игры в крестики-нолики
def play_tic_tac_toe(chat_id, position):
    game = games[chat_id]
    board = game['board']
    turn = game['turn']

    if board[position] == ' ':
        board[position] = turn
        print_board(chat_id)

        if check_winner(board, turn):
            bot.send_message(chat_id, f"Игра окончена! Победил {turn}.")
            del games[chat_id]
            return
        elif ' ' not in board:
            bot.send_message(chat_id, "Игра окончена! Ничья.")
            del games[chat_id]
            return

        game['turn'] = 'O' if turn == 'X' else 'X'
        bot.edit_message_text(f"Ходит {game['turn']}.", chat_id, game['message_id'])
        bot.edit_message_reply_markup(chat_id, game['message_id'], reply_markup=generate_tic_tac_toe_markup(chat_id))

# Отображение текущего состояния игрового поля крестиков-ноликов
def print_board(chat_id):
    game = games[chat_id]
    board = game['board']
    board_str = f" {board[0]} | {board[1]} | {board[2]}\n"
    board_str += "-----------\n"
    board_str += f" {board[3]} | {board[4]} | {board[5]}\n"
    board_str += "-----------\n"
    board_str += f" {board[6]} | {board[7]} | {board[8]}\n"
    bot.edit_message_text(board_str, chat_id, game['message_id'], reply_markup=generate_tic_tac_toe_markup(chat_id))

# Проверка на победу
def check_winner(board, mark):
    win_combinations = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Горизонтальные линии
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Вертикальные линии
        (0, 4, 8), (2, 4, 6)             # Диагонали
    )
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == mark:
            return True
    return False

# Команда /guess_who
@bot.message_handler(commands=['guess_who'])
def guess_who(message):
    characters = ['Гарри Поттер', 'Шерлок Холмс', 'Микки Маус', 'Дарт Вейдер', 'Гермиона Грейнджер']
    chosen_character = random.choice(characters)
    bot.send_message(message.chat.id, f"Думаю о персонаже... Попробуйте угадать, кто это! "
                                      f"(Кого мог загадать: {' '.join(characters)})")

# Обработчик ввода пользователем для угадывания персонажа
@bot.message_handler(func=lambda message: True)
def handle_guess(message):
    characters = ['Гарри Поттер', 'Шерлок Холмс', 'Микки Маус', 'Дарт Вейдер', 'Гермиона Грейнджер']
    chosen_character = random.choice(characters)
    if message.text in characters:
        if message.text == chosen_character:
            bot.send_message(message.chat.id, "Поздравляю! Вы угадали!")
        else:
            bot.send_message(message.chat.id, f"К сожалению, это не {message.text}. Попробуйте еще раз!")
    else:
        bot.send_message(message.chat.id, "Попробуйте угадать персонажа, используя кнопки с вариантами.")

# Запуск бота
bot.polling()
