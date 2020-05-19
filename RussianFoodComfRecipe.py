import json
from typing import List
from Ingredient import Ingredient
from bs4 import BeautifulSoup
from Recipe import Recipe


def decode_russian_food_com(html_str: str) -> Recipe:
        soup = BeautifulSoup(html_str, 'html.parser')
        name = soup.find("h1", {"class": "title"}).get_text().strip()
        ingredients1 = soup.find_all("tr", {"class": "ingr_tr_0"})
        ingredients2 = soup.find_all("tr", {"class": "ingr_tr_1"})
        ingredients = [Ingredient(ingredient.get_text().strip().split(' -')) for ingredient in
                            ingredients1 + ingredients2]
        directions = [recipe.get_text().strip() for recipe in soup.find_all("div", {"class": "step_n"})]
        description = recipe = \
            soup.find_all("table", {"class": "recipe_new"})[0].find_all("td", {"class": "padding_l padding_r"})[
                0].find(
                id="ib_s_e_2").next_element.get_text()
        image_url = soup.find("table", {"class": "main_image"}).find("img")["src"]
        return Recipe(name, image_url, description, ingredients, directions)
