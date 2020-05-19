from bs4 import BeautifulSoup
import requests
import json
import os
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
    response = answer.json()
    print(response)


s = requests.Session()
recipes_quantity = 100
counter = 1
if not os.path.exists('./out'):
    os.mkdir('./out')
while recipes_quantity > 0:
    try:
        print('.', end='')
        bytes_url = s.get("https://www.russianfood.com/recipes/recipe.php?rid={0}".format(counter))
        counter += 1
        html_doc = bytes_url.text

        soup = BeautifulSoup(html_doc, 'html.parser')

        t = decode_russian_food_com(html_doc)

        with open('./out/out_recipe{0}.txt'.format(recipes_quantity), 'w') as f:
            f.write(t.to_json())
            recipes_quantity -= 1
            print('\n', recipes_quantity)
    except Exception:
        pass
