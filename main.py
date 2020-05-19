from bs4 import BeautifulSoup
import requests
import json
import os
from os import listdir
from os.path import isfile, join
import sys
import time
from RussianFoodComfRecipe import decode_russian_food_com

proxies = {
    "https": "https://144.202.11.54:8080",
    "http": "82.119.170.106:8080"
}


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
    for filename in onlyfiles:
        with open(join(out_dir, filename), 'r') as f:
            send(f.read())

id_list = [156189, 152510, 134935, 121118, 123433, 156089, 137206, 116665, 102711, 121844,
            152213, 58655, 126678, 121626, 130693, 140838, 122737, 134924, 141692, 123559, 136031, 117690, 142942,
            132454, 131921, 127181, 132593, 137701, 107064, 146941, 142047, 147963, 131921, 141929, 132716]
if not os.path.exists('./out'):
    os.mkdir('./out')
for recipe_id in id_list:
    if os.path.exists('./out/out_recipe{0}.json'.format(recipe_id)):
        continue
    time.sleep(5)
    print('.', end='')
    sys.stdout.flush()
    bytes_url = requests.get("https://www.russianfood.com/recipes/recipe.php?rid={0}".format(recipe_id))
    html_doc = bytes_url.text
    print(recipe_id,'\n')

    soup = BeautifulSoup(html_doc, 'html.parser')

    t = decode_russian_food_com(html_doc)

    with open('./out/out_recipe{0}.json'.format(recipe_id), 'w') as f:
        f.write(t.to_json())


