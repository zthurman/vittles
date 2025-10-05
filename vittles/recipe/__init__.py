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

REQUIRED_KEYS = ["Title", "Ingredients", "Directions"]


class JsonRecipeImporter:
    def __init__(self, input_recipe: str):
        with open(input_recipe, "r") as file:
            self.input_recipe = json.load(file)
        self.recipe_valid = self.verify_input()
        assert self.recipe_valid, f"{self.recipe_keys_message()}"

    def recipe_keys_message(self):
        msg = f"A recipe must have: {self.required_keys()}"
        return msg

    def required_keys(self):
        return REQUIRED_KEYS

    def verify_input(self):
        if all(key in self.input_recipe for key in self.required_keys()):
            return True
        else:
            return False
