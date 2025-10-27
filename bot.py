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

    # Используем общую функцию для создания карточек
    create_word_cards(message)


def create_word_cards(message):
    """Создает новые карточки слов (общая функция для /start и NEXT)"""
    user_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=2)

    # ОДИН вызов функции
    random_id = random.randint(1027, 2006)
    wrong_attempts = session.query(sql.UserWord).filter(sql.UserWord.word_id == random_id).first()
    if wrong_attempts and wrong_attempts.wrong_attempts > 3:
        random_id = random.randint(1027, 2006)
    word_data = target_translate(id=random_id)
    target_word = word_data.eng_word
    translate = word_data.translation

    # Добавляем слово в словарь пользователя
    new_word(user_id, word_data.id)

    # СОЗДАЕМ НОВЫЙ список кнопок каждый раз
    buttons = []

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


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    """Обработчик кнопки Дальше ⏭"""
    create_word_cards(message)


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    """Обработчик кнопки Добавить слово ➕"""
    bot.send_message(message.chat.id, "Функция добавления слова")


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    """Обработчик кнопки Удалить слово🔙"""
    bot.send_message(message.chat.id, "Функция удаления слова")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    """Обработчик выбора слова (основная логика)"""
    # Игнорируем сервисные команды - они уже обработаны выше
    if message.text in [Command.NEXT, Command.ADD_WORD, Command.DELETE_WORD]:
        return

    # Получаем данные из состояния
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        translate_word = data['translate_word']

    # Сравниваем с сообщением пользователя
    if message.text == target_word:
        word_id = session.query(sql.Word).filter(sql.Word.eng_word == target_word).first()
        session.query(sql.UserWord).filter(sql.UserWord.word_id == word_id.id).update({'wrong_attempts': sql.UserWord.wrong_attempts + 1},
            synchronize_session=False)
        session.commit()
        bot.send_message(message.chat.id, "✅ Правильно!")
    else:
        bot.send_message(message.chat.id, f"❌ Неправильно. Правильный ответ: {target_word}")

    # Ждем команду NEXT для следующего слова
    bot.send_message(message.chat.id, "Нажми 'Дальше ⏭' для следующего слова")


if __name__ == '__main__':
    bot.polling()