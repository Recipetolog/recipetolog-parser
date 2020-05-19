import json
from typing import List, Tuple
from Ingredient import Ingredient
from bs4 import BeautifulSoup
from Recipe import Recipe
import re

pattern = re.compile('([А-Яа-я ]+)[-–—‒―⸺⸻](.+)')


def split_ingredient(ingr: str) -> Tuple[str, str]:
    groups = pattern.findall(ingr)
    if len(groups) == 0:
        if ingr.strip()[-1] == ':':
            return '', ''
        else:
            return ingr, ''
    return groups[0][0].strip(), groups[0][1].strip()


def remove_digits(step: str) -> str:
    return step[step.find('.') + 1:].strip()


def decode_russian_food_com(html_str: str, source: str) -> Recipe:
    soup = BeautifulSoup(html_str, 'html.parser')
    name = soup.find("h1", {"class": "title"}).get_text().strip()
    ingredients1 = soup.find_all("tr", {"class": "ingr_tr_0"})
    ingredients2 = soup.find_all("tr", {"class": "ingr_tr_1"})
    ingredients_temp = [Ingredient(split_ingredient(ingredient.get_text())) for ingredient in
                        ingredients1 + ingredients2]
    ingredients = [ingredient for ingredient in ingredients_temp if len(ingredient.get_ingredient_name()) > 0]
    how_dirs = [remove_digits(recipe.get_text().strip()) for recipe in soup.find(id='how').find_all('p') if
                len(recipe.get_text()) > 0 and recipe.get_text()[0].isdigit()]
    directions = [recipe.get_text().strip() for recipe in soup.find_all("div", {"class": "step_n"})]
    if len(how_dirs) > 0:
        directions = how_dirs
    description = recipe = \
        soup.find_all("table", {"class": "recipe_new"})[0].find_all("td", {"class": "padding_l padding_r"})[
            0].find(
            id="ib_s_e_2").next_element.get_text()
    image_url = soup.find("table", {"class": "main_image"}).find("img")["src"]
    return Recipe(name, image_url, description, ingredients, directions, source)
