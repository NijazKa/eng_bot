from pyexpat.errors import messages
import random
from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

import sql
from config import TOKEN
from sql import session

TOKEN = TOKEN
state_storage = StateMemoryStorage()
bot = TeleBot(TOKEN)

buttons = []

class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'

class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()

# функция получения рандомного слова
def random_word():
    pass

def new_user(uid):
    if session.query(sql.User).filter(sql.User.tg_id == uid).all():
        print('пользователь есть')
    else:
        print('нет пользователя')



@bot.message_handler(commands=['start'])
def send_hello(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name else ""
    username = message.from_user.username if message.from_user.username else ""
    full_name = f"{first_name} {last_name}".strip()
    if session.query(sql.User).filter(sql.User.tg_id == user_id).all():
        bot.send_message(user_id, f"Привет, {full_name}! С возвращением")
        print(f"User ID: {user_id}, Name: {full_name}, Username: @{username}")
    else:
        user = sql.User(tg_id=user_id, name=first_name)
        session.add(user)
        session.commit()
        bot.send_message(user_id, f"Привет, {full_name}! Давай учиться английскому.")

    markup = types.ReplyKeyboardMarkup(row_width=2)

    target_word = 'Peace'
    translate = 'Мир'
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    others = ['Green', 'White', 'Hello', 'Car']
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others


# @bot.message_handler(commands=['button'])
# def button_message(message):
#     markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1=types.KeyboardButton("Кнопка")
#     markup.add(item1)
#     bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

if __name__ == '__main__':
    bot.polling()