from pyexpat.errors import messages

from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from config import TOKEN

TOKEN = TOKEN
state_storage = StateMemoryStorage()
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

if __name__ == '__main__':
    bot.polling()