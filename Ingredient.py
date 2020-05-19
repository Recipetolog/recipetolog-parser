import json
from typing import List


class Ingredient:
    def __init__(self, src: List[str]):
        self.name, self.amount = src[0].strip(), src[1].strip()
        self.name = self.name.replace('\t', ' ').strip()

    def get_ingredient_name(self) -> str:
        return self.name

    def get_amount(self) -> str:
        return self.amount

    def to_json(self):
        return {'name': self.name, 'amount': self.amount}

    def __repr__(self) -> str:
        return self.get_ingredient_name() + ' - ' + self.get_amount()
