"""

vittles, recipe book generator
Copyright (C) [2025] [Zechariah Thurman]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import json

from vittles.ingredient import Ingredient

REQUIRED_KEYS = [
    "Title",
    "Prep Time",
    "Cook Time",
    "Servings",
    "Ingredients",
    "Directions",
]


class JsonRecipeImporter:
    def __init__(self, input_recipe: str):
        with open(input_recipe, "r") as file:
            self.recipe_dict = json.load(file)
        self.recipe_valid = self.verify_input()
        self.title = self.recipe_dict["Title"]
        self.preptime = self.recipe_dict["Prep Time"]
        self.cooktime = self.recipe_dict["Cook Time"]
        self.servings = self.recipe_dict["Servings"]
        self.ingredients = self.get_ingredients()
        self.directions = self.recipe_dict["Directions"]

    def recipe_keys_message(self):
        msg = f"A recipe must have: {self.required_keys()}"
        return msg

    def required_keys(self):
        return REQUIRED_KEYS

    def verify_input(self):
        if all(key in self.recipe_dict for key in self.required_keys()):
            return True
        else:
            raise ValueError(f"{self.recipe_keys_message()}")

    def get_ingredients(self):
        ingredients = list()
        for ingredient_str in self.recipe_dict["Ingredients"]:
            ingredients.append(Ingredient(ingredient_str=ingredient_str))
        return ingredients
