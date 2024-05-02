import requests
from bs4 import BeautifulSoup
import random

import re

import json

headers = json.loads(open("headers.json", "r").read())

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

print(get_random_url_from_list("https://letterboxd.com/thps/list/test/"))
