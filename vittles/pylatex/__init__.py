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
import json

from pylatex import Command, Document, Section, Package, Enumerate, Tabular
from pylatex.base_classes import Environment, ContainerCommand, CommandBase, LatexObject
from pylatex.utils import NoEscape

from vittles.recipe import JsonRecipeImporter
from vittles.pylatex.extensions import (
    Title,
    MakeTitle,
    ClearPage,
    TableOfContents,
    Recipe,
    Ingredients,
    Preparation,
    Portion,
    Step,
)


class Vittles(Document):
    def __init__(
        self,
        recipe_path: str = "json",
        image_path: str = "img",
        title_image_name: str = "title.jpg",
        image_params_name: str = "image-params.json",
    ):
        super().__init__()
        self.recipe_path = recipe_path
        self.recipe_path_contents = sorted(os.listdir(self.recipe_path))
        self.image_path = image_path
        self.image_path_contents = os.listdir(self.image_path)
        self.title_image_name = title_image_name
        self.image_params_name = image_params_name
        self.load_image_params()
        self.default_image_scale = 0.1
        self.default_image_rotation = None
        self.find_available_categories()
        self.find_available_recipes()

    def title_image(self):
        if self.title_image_name in self.image_path_contents:
            return os.path.abspath(f"{self.image_path}/{self.title_image_name}")
        else:
            return None

    def load_image_params(self):
        if self.image_params_name in self.image_path_contents:
            image_params_file = os.path.abspath(
                f"{self.image_path}/{self.image_params_name}"
            )
            with open(image_params_file, "r") as file:
                self.image_params = json.load(file)
        else:
            self.image_params = None

    def find_available_categories(self):
        self.available_categories = list()
        for content in self.recipe_path_contents:
            if os.path.isdir(os.path.abspath(f"{self.recipe_path}/{content}")):
                for each in os.listdir(
                    os.path.abspath(f"{self.recipe_path}/{content}")
                ):
                    if each.endswith(".json"):
                        self.available_categories.append(content)

    def find_available_recipes(self):
        self.available_recipes = dict()
        if len(self.available_categories) > 0:
            for category in self.available_categories:
                self.available_recipes[category.title()] = os.listdir(
                    f"{self.recipe_path}/{category}"
                )
        else:
            recipes = list()
            for potential_recipe in os.listdir(self.recipe_path):
                if potential_recipe.endswith(".json"):
                    recipes.append(potential_recipe)
            self.available_recipes["Recipes"] = recipes

    def add_packages_to_preamble(self):
        self.preamble.append(Package("lettrine"))  # for steps to show up
        self.preamble.append(Package("cookingsymbols"))
        self.preamble.append(Package("xcookybooky"))

    def append_centered_image(
        self,
        append_target,
        image,
        image_rotation: int = None,
        image_scale: float = None,
        shorten_following_vspace: int = None,
    ):
        append_target.append(NoEscape(r"\begin{center}"))
        options = list()
        if image_rotation:
            options.append(f"angle={image_rotation}")
        if image_scale:
            options.append(f"scale={image_scale}")
        append_target.append(
            NoEscape(rf"\includegraphics[{",".join(options)}]{{{image}}}")
        )
        append_target.append(NoEscape(r"\end{center}"))
        if shorten_following_vspace:
            append_target.append(NoEscape(rf"\vspace{{{shorten_following_vspace}em}}"))

    def add_title_to_preamble(self):
        if self.title_image():
            self.preamble.append(NoEscape(r"\title{"))
            self.preamble.append(NoEscape(r"Vittles"))
            if self.image_params:
                stripped_title_image = self.title_image_name.split(".")[0]
                title_image_params = self.image_params[stripped_title_image]
                self.append_centered_image(
                    append_target=self.preamble,
                    image=self.title_image(),
                    image_scale=title_image_params["scale"],
                    image_rotation=title_image_params["rotation"],
                )
            else:
                # print("No image params found, trying defaults")
                self.append_centered_image(
                    append_target=self.preamble,
                    image=self.title_image(),
                    image_scale=self.default_image_scale,
                    image_rotation=self.default_image_rotation,
                )
            self.preamble.append(NoEscape(r"}"))
        else:
            self.preamble.append(Title("Vittles"))

    def add_author_to_preamble(self):
        self.preamble.append(Command("author", "Zam"))

    def add_date_to_preamble(self):
        self.preamble.append(Command("date", NoEscape(r"\today")))

    def make_title(self):
        self.append(MakeTitle())
        self.append(ClearPage())

    def make_toc(self):
        self.append(TableOfContents())
        self.append(ClearPage())

    def assemble_recipe_options(self, recipe: Recipe):
        recipe_options = list()
        recipe_options.append(NoEscape(rf"portion={{{recipe.servings}}} servings"))
        recipe_options.append(NoEscape(rf"preparationtime={{{recipe.preptime}}}"))
        recipe_options.append(NoEscape(rf"bakingtime={{{recipe.cooktime}}}"))
        return recipe_options

    def fill_document(self):
        self.add_packages_to_preamble()
        self.add_title_to_preamble()
        self.add_author_to_preamble()
        self.add_date_to_preamble()
        self.make_title()
        self.make_toc()
        for category, recipes in self.available_recipes.items():
            with self.create(Section(category)):
                for recipe_file in recipes:
                    recipe = JsonRecipeImporter(
                        input_recipe=f"{self.recipe_path}/{category.lower()}/{recipe_file}"
                    )
                    with self.create(
                        Recipe(options=self.assemble_recipe_options(recipe))
                    ):
                        raw_title = rf"{{{recipe.title}}}"
                        self.append(NoEscape(raw_title))
                        recipe_image = os.path.abspath(
                            f"{self.image_path}/{recipe_file.split('.')[0]}.jpg"
                        )
                        if os.path.exists(recipe_image):
                            print(f"recipe image exists: {recipe_image}")
                            # TODO: neckbeard hax, clean up next line
                            image_param_key = recipe_image.split(".")[0].split("/")[-1]
                            recipe_image_params = self.image_params[image_param_key]
                            self.append_centered_image(
                                append_target=self,
                                image=recipe_image,
                                image_scale=recipe_image_params["scale"],
                                image_rotation=recipe_image_params["rotation"],
                                shorten_following_vspace=recipe_image_params[
                                    "following_vspace"
                                ],
                            )
                        else:
                            print(f"recipe image does NOT exist: {recipe_file}")
                        with self.create(Preparation()):
                            with self.create(Enumerate()) as enum:
                                for step in recipe.directions:
                                    enum.add_item(step)
                            # I don't know why Step horks the tex compile
                            # I think I'm doing what xcookybooky tells
                            # me to do
                            # for step in recipe.directions:
                            #    self.append(Step(data=step))
                        with self.create(Ingredients()):
                            with self.create(Tabular("c l")) as table:
                                for ingredient in recipe.ingredients:
                                    table.add_row(
                                        f"{ingredient.quantity} {ingredient.unit}",
                                        f"{ingredient.name}",
                                    )
                    self.append(ClearPage())
