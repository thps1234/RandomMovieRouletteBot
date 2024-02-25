import telebot
from telebot import types

bot = telebot.TeleBot('6470319699:AAFZAv2AulBCohVSY4HVkKschZcJwudnjPs')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Roll")
    markup.add(btn)
    bot.send_message(message.from_user.id, "Test", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Test')


bot.polling(none_stop=True, interval=0)