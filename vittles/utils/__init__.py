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

    def writeToJson(self):
        with open(self.filename(), "w") as json_file:
            json.dump(self.input_recipe, json_file, indent=4)


class ImageParamsAdder:
    def __init__(self, image_params_dict: dict, image_dir: str = "img"):
        self.image_params_dict = image_params_dict
        self.image_dir = os.path.abspath(image_dir)

    def filename(self):
        filename = f"{self.image_dir}/image-params.json"
        return filename

    def writeToJson(self):
        with open(self.filename(), "w") as json_file:
            json.dump(self.image_params_dict, json_file, indent=4)
