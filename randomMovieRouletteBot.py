import telebot
from telebot import types

bot = telebot.TeleBot('6470319699:AAFZAv2AulBCohVSY4HVkKschZcJwudnjPs')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Roll")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Roll", reply_markup=markup)

bot.polling(none_stop=True, interval=0)