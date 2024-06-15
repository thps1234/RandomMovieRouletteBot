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
lc_url_re_long = ("^" + re.escape("letterboxd.com/")
                  + "[0-9a-z_-]{1,100}" + re.escape("/list/") + "[0-9a-z_-]{1,100}" + re.escape("/"))
lc_url_re_long_https = ("^" + re.escape("https://letterboxd.com/")
                        + "[0-9a-z_-]{1,100}" + re.escape("/list/") + "[0-9a-z_-]{1,100}" + re.escape("/"))
lc_url_re_short = re.escape("https://boxd.it/") + "[0-9a-zA-Z]{5}"


#returns a dictionary of movie attributes by its URL
def get_movie_attrs(i_url):
    lt_attr = dict()
    page = requests.get(i_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    lv_duration = re.search('runTime: [0-9]{1,4}', str(soup))
    lv_duration = str(soup)[lv_duration.regs[0][0]:lv_duration.regs[0][1]].split(' ')[1]
    lt_attr["Duration"] = divmod(int(lv_duration), 60)
    lt_attr["Description"] = soup.find("meta", property="og:description").attrs["content"]
    lt_attr["Title"] = soup.find("meta", property="og:title").attrs["content"]
    lt_attr["Directed by"] = soup.find("meta", content="Directed by").next.attrs["content"]
    lt_attr["Average rating"] = soup.find("meta", content="Average rating").next.attrs["content"].split(' ')[0]
    lt_attr["Image"] = soup.find("meta", property="og:image").attrs["content"]
    lv_origtitle = soup.find("h2", class_="originalname")
    if lv_origtitle is not None:
        lt_attr["Original Title"] = soup.find("h2", class_="originalname").contents[0]
    return lt_attr


#picks a random movie from a list
def get_random_url_from_list(i_url):
    page = requests.get(i_url, headers=headers)
    i_url = page.url #making a big URL out of short
    soup = BeautifulSoup(page.content, "html.parser")
    lv_description = soup.find_all("meta")[3].attrs["content"]
    lv_number = int(lv_description.split(" ", 4)[3].replace(",", ""))
    lv_index = random.randrange(lv_number)
    lv_page = lv_index // 100 + 1
    lv_num_on_page = lv_index % 100
    lv_url = i_url + "page/" + str(lv_page)
    page = requests.get(lv_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    return "https://letterboxd.com" + \
        soup.find_all("div", class_="really-lazy-load")[lv_num_on_page].attrs["data-target-link"]


#formatting the message
def get_message(i_movie_url):
    lt_attrs = get_movie_attrs(i_movie_url)
    lt_message = [lt_attrs["Image"]]
    if "Original Title" in lt_attrs:
        lv_name = lt_attrs["Original Title"] + "/" + lt_attrs["Title"]
    else:
        lv_name = lt_attrs["Title"]
    lt_message.append("<b><a href=\"" + i_movie_url + "\">" + lv_name + "</a></b>" + "\n" + \
                      "<b>Directed by</b> " + lt_attrs["Directed by"] + "\n" + \
                      "<b>Duration:</b> " + str(lt_attrs["Duration"][0]) + " h. " + str(lt_attrs["Duration"][1]) + " min. \n" + \
                      "<b>Rating:</b> " + lt_attrs["Average rating"] + "\n\n" + \
                      lt_attrs["Description"])
    return lt_message


#message handling: drawing keyboard at start
#or picking a random movie from a given list
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, text="<b>Choose from list or send URL:</b>",
                         reply_markup=keyboard, parse_mode="HTML")
    elif re.match(lc_url_re_long, message.text) or re.match(lc_url_re_long_https, message.text):
        bot.send_dice(message.from_user.id)
        lt_message = get_message(get_random_url_from_list(message.text))
        bot.send_photo(message.from_user.id, lt_message[0], lt_message[1], parse_mode="HTML")
        bot.send_message(message.from_user.id, text="<b>Choose from list or send URL:</b>",
                         reply_markup=keyboard, parse_mode="HTML")
    elif re.search(lc_url_re_short, message.text) is not None:
        bot.send_dice(message.from_user.id)
        lv_url = message.text[
                    re.search(lc_url_re_short, message.text).regs[0][0]:
                    re.search(lc_url_re_short, message.text).regs[0][1]
                 ]
        lt_message = get_message(get_random_url_from_list(lv_url))
        bot.send_photo(message.from_user.id, lt_message[0], lt_message[1], parse_mode="HTML")
        bot.send_message(message.from_user.id, text="<b>Choose from list or send URL:</b>",
                         reply_markup=keyboard, parse_mode="HTML")
    else:
        bot.send_message(message.from_user.id, "Please check your URL and try again")


#button handling: picking a movie from a chosen list
#and drawing a keyboard again for a reroll
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    bot.send_dice(call.message.chat.id)
    lt_message = get_message(get_random_url_from_list(lt_lists[call.data]))
    bot.send_photo(call.message.chat.id, lt_message[0], lt_message[1], parse_mode="HTML")
    bot.send_message(call.message.chat.id, text="<b>Choose from list or send URL:</b>",
                     reply_markup=keyboard, parse_mode="HTML")


bot.polling(none_stop=True, interval=0)
