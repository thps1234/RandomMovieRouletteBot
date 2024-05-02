import requests
from bs4 import BeautifulSoup
import random

import re

import json

headers = json.loads(open("headers.json", "r").read())

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
    return "https://letterboxd.com" + \
        soup.find_all("div", class_="really-lazy-load")[lv_num_on_page].attrs["data-target-link"]


lc_url_re1 = ("^" + re.escape("letterboxd.com/")
              + "[0-9a-z_-]{1,100}" + re.escape("/list/") + "[0-9a-z_-]{1,100}" + re.escape("/"))
lc_url_re2 = ("^" + re.escape("https://letterboxd.com/")
              + "[0-9a-z_-]{1,100}" + re.escape("/list/") + "[0-9a-z_-]{1,100}" + re.escape("/"))
lc_url_re3 = re.escape("https://boxd.it/") + "[0-9a-zA-Z]{5}"

lv_url = "Dale Cooper's Picks https://boxd.it/uKaAG"

if re.search(lc_url_re3, lv_url) is not None:
    print(get_random_url_from_list(lv_url[re.search(lc_url_re3, lv_url).regs[0][0]:re.search(lc_url_re3, lv_url).regs[0][1]]))


if re.match(lc_url_re1, lv_url) or re.match(lc_url_re2, lv_url) or re.match(lc_url_re3, lv_url):
    print(get_random_url_from_list(lv_url[re.search(lc_url_re3, lv_url).regs[0][0]:re.search(lc_url_re3, lv_url).regs[0][1]]))
