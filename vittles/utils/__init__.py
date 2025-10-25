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

import os
from pathlib import Path
import json


class RecipeAdder:
    def __init__(self, recipe_dict: dict, category: str = None):
        self.input_recipe = recipe_dict
        self.category = category

    def filename(self):
        this_path = Path(__file__)
        target_path = this_path.parent.parent.parent
        if self.category is not None:
            recipe_dir = f"{target_path}/json/{self.category}"
        else:
            recipe_dir = f"{target_path}/json"
        os.makedirs(recipe_dir, exist_ok=True)
        filename = (
            f"{recipe_dir}/{self.input_recipe["Title"].lower().replace(" ", "-")}.json"
        )
        return filename

    def writeToExamples(self):
        with open(self.filename(), "w") as json_file:
            json.dump(self.input_recipe, json_file, indent=4)
