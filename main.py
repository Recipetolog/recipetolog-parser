from bs4 import BeautifulSoup
import requests
import json
import os
from os import listdir
from os.path import isfile, join
import sys
import time
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
    for filename in onlyfiles:
        with open(join(out_dir, filename), 'r') as f:
            send(f.read())


id_list = [156189, 152510, 134935, 121118, 123433, 156089, 137206, 102711, 121844, 138963, 131965, 151327, 123940,
           152213, 58655, 126678, 121626, 130693, 140838, 122737, 134924, 141692, 123559, 136031, 117690, 142942,
           132454, 131921, 127181, 132593, 137701, 107064, 146941, 142047, 147963, 131921, 141929, 132716, 138276,
           146833, 136624, 129231, 139537, 125424, 149096, 129003, 134420, 129110, 145571, 122889]
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
