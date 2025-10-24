from pyexpat.errors import messages
import random
from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

from config import TOKEN
import sql
from sql import session
from functions import random_word, target_translate, new_word

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

    target_word = target_translate.eng_word
    translate = target_translate.translate
    new_word(user_id, target_word[2])

    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    others = random_word()
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


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    # Получаем данные из состояния
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']  # английское слово
        translate_word = data['translate_word']  # русский перевод

    # Сравниваем с сообщением пользователя
    if message.text == target_word:  # если пользователь выбрал правильное английское слово
        bot.send_message(message.chat.id, "✅ Правильно!")
        # Генерируем следующее слово
        send_hello(message)
    else:
        bot.send_message(message.chat.id, f"❌ Неправильно. Правильный ответ: {target_word}")
        # Также генерируем следующее слово
        send_hello(message)

@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    #create_cards(message)
    pass

if __name__ == '__main__':
    print(random_word())
    bot.polling()