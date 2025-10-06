"""

Copyright [2025] [Zechariah Thurman]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

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
        assert self.recipe_valid, f"{self.recipe_keys_message()}"
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
            return False

    def get_ingredients(self):
        ingredients = list()
        for ingredient_str in self.recipe_dict["Ingredients"]:
            ingredients.append(Ingredient(ingredient_str=ingredient_str))
        return ingredients
