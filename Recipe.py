import json
from typing import List

from Ingredient import Ingredient


class Recipe:
    def __init__(self, name: str, image_url: str, description: str, ingredients: List[Ingredient],
                 directions: List[str], source: str = ''):
        if image_url[0] == '/':
            image_url = 'https:' + image_url
        self.image_url = image_url
        self.description = description
        self.name = name
        self.ingredients = ingredients
        self.directions = directions
        self.source = source

    def get_name(self) -> str:
        return self.name

    def get_image_url(self) -> str:
        return self.image_url

    def get_description(self) -> str:
        return self.description

    def get_ingredients(self) -> List[Ingredient]:
        return self.ingredients

    def get_directions(self) -> List[str]:
        return self.directions

    def to_json(self):
        return json.dumps(self, default=lambda o: {'name': self.get_name(), 'imageUrl': self.get_image_url(),
                                                   'description': self.get_description(),
                                                   'ingredients': {i.get_ingredient_name(): i.get_amount() for i in
                                                                   self.get_ingredients()},
                                                   'directions': self.get_directions(),
                                                   'source': self.source})
