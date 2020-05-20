from typing import List

from bs4 import BeautifulSoup
import requests
import json
import os
from os import listdir
from os.path import isfile, join
import sys
import time
import re
from RussianFoodComfRecipe import decode_russian_food_com


def send(json_str: str):
    url = 'https://recipetolog.herokuapp.com/recipes'
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}
    answer = requests.post(url, data=json_str, headers=headers)
    print(answer)


def send_all():
    out_dir = './out'
    onlyfiles = [f for f in listdir(out_dir) if isfile(join(out_dir, f))]
    print(len(onlyfiles))
    # for filename in onlyfiles:
    #     with open(join(out_dir, filename), 'r') as f:
    #         send(f.read())


def get_id(url: str) -> int:
    rid = pattern.findall(url)
    return int(rid[0])


def get_id_from_list(url: str) -> List[int]:
    bytes_url = requests.get(url)
    html_doc = bytes_url.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    recipe_list = soup.find('div', {'class': 'recipe_list_new'}).find_all('div', {'class': 'title'})
    ar = [get_id(el.find('a')['href']) for el in recipe_list]
    return ar


pattern = re.compile('rid=([0-9]+)')

fids = [6, 5, 1535, 8, 2, 9]

accum = []
for i in fids:
    time.sleep(5)
    print('.', end='')
    sys.stdout.flush()
    accum += get_id_from_list('https://www.russianfood.com/recipes/bytype/?fid={0}'.format(i))
print(accum)

# send_all()

print('')

id_list = set(accum)
print(len(id_list))
if not os.path.exists('./out'):
    os.mkdir('./out')
for recipe_id in id_list:
    if os.path.exists('./out/out_recipe{0}.json'.format(recipe_id)):
        continue
    time.sleep(5)
    print('.', end='')
    sys.stdout.flush()
    url = "https://www.russianfood.com/recipes/recipe.php?rid={0}".format(recipe_id)
    bytes_url = requests.get(url)
    html_doc = bytes_url.text
    print(recipe_id, '\n')

    soup = BeautifulSoup(html_doc, 'html.parser')

    t = decode_russian_food_com(html_doc, url)

    with open('./out/out_recipe{0}.json'.format(recipe_id), 'w') as f:
        print(t.get_ingredients(), '\n')
        print(t.get_directions(), '\n')
        f.write(t.to_json())
