import telebot
from telebot import types

import re

import json

import requests
from bs4 import BeautifulSoup
import random


#initialization: bot, headers and keyboard
bot = telebot.TeleBot(open("token.txt", "r").read())

headers = json.loads(open("headers.json", "r").read())

lt_lists = json.loads(open("lists.json", "r").read())

keyboard = types.InlineKeyboardMarkup()
for i in lt_lists.keys():
    key = types.InlineKeyboardButton(text=i, callback_data=i)
    keyboard.add(key)

#regexes for a valid list URL
lc_url_re1 = ("^" + re.escape("letterboxd.com/")
              + "[0-9a-z_-]{1,100}" + re.escape("/list/") + "[0-9a-z_-]{1,100}" + re.escape("/"))
lc_url_re2 = ("^" + re.escape("https://letterboxd.com/")
              + "[0-9a-z_-]{1,100}" + re.escape("/list/") + "[0-9a-z_-]{1,100}" + re.escape("/"))


#returns a dictionary of movie attributes by its URL
def get_movie_attrs(i_url):
    lt_attr = dict()
    page = requests.get(i_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    element = soup.find("section", class_="film-header-lockup")
    if len(element.contents[3].contents) == 5:
        lt_attr["Name"] = element.contents[1].text
        lt_attr["Directed by"] = element.contents[3].contents[3].text
        lt_attr["Year"] = element.contents[3].contents[1].text
    else:
        lt_attr["Name"] = element.contents[1].text
        lt_attr["Original Name"] = element.contents[3].contents[3].text
        lt_attr["Directed by"] = element.contents[3].contents[5].text
        lt_attr["Year"] = element.contents[3].contents[1].text
    return lt_attr


#picks a random movie from a list
def get_random_url_from_list(i_url):
    page = requests.get(i_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    lv_description = soup.find_all("meta")[3].attrs["content"]
    lv_number = int(lv_description.split(" ", 4)[3].replace(",", ""))
    lv_index = random.randrange(lv_number)
    lv_page = lv_index // 100 + 1
    lv_num_on_page = lv_index % 100 + 1
    lv_url = i_url + "/page/" + str(lv_page)
    page = requests.get(lv_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    return "https://letterboxd.com/" + \
        soup.find_all("div", class_="really-lazy-load")[lv_num_on_page].attrs["data-target-link"]


#formatting the message
def get_message(i_movie_url):
    lv_message = "<b><a href=\"" + i_movie_url + "\">" + get_movie_attrs(i_movie_url)["Name"] + "</a></b>" + "\n" + \
                 "Directed by " + get_movie_attrs(i_movie_url)["Directed by"] + "\n" \
                 "Year: " + get_movie_attrs(i_movie_url)['Year']
    return lv_message


#message handling: drawing keyboard at start
#or picking a random movie from a given list
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, text="<b>Choose from list or send URL:</b>",
                         reply_markup=keyboard, parse_mode="HTML")
    elif re.match(lc_url_re1, message.text) or re.match(lc_url_re2, message.text):
        bot.send_message(message.from_user.id,
                         get_message(get_random_url_from_list(message.text)), parse_mode="HTML")
        bot.send_message(message.from_user.id, text="<b>Choose from list or send URL:</b>",
                         reply_markup=keyboard, parse_mode="HTML")
    else:
        bot.send_message(message.from_user.id, "Please check your URL and try again")


#button handling: picking a movie from a chosen list
#and drawing a keyboard again for a reroll
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    bot.send_message(call.message.chat.id,
                     get_message(get_random_url_from_list(lt_lists[call.data])), parse_mode="HTML")
    bot.send_message(call.message.chat.id, text="<b>Choose from list or send URL:</b>",
                     reply_markup=keyboard, parse_mode="HTML")


bot.polling(none_stop=True, interval=0)
