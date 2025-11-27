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
    def __init__(self, recipe_path: str = "json", image_path: str = "img"):
        super().__init__()
        self.recipe_path = recipe_path
        self.recipe_path_contents = os.listdir(self.recipe_path)
        self.image_path = image_path
        self.image_path_contents = os.listdir(self.image_path)
        self.find_available_categories()
        self.find_available_recipes()

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

    def add_title_author_date_to_preamble(self):
        title_image = os.path.abspath(f"{self.image_path}/title.jpg")
        self.append(NoEscape(r"\title{"))
        self.append(NoEscape(r"Vittles"))
        self.append(NoEscape(r"\begin{center}"))
        self.append(NoEscape(rf"\includegraphics[angle=-90,scale=0.1]{{{title_image}}}"))
        self.append(NoEscape(r"\end{center}"))
        self.append(NoEscape(r"}"))
        #self.preamble.append(Title("Vittles", options=NoEscape(rf"\includegraphics[scale=0.1]{{{title_image}}}")))
        self.preamble.append(Command("author", "Zam"))
        self.preamble.append(Command("date", NoEscape(r"\today")))

    def make_title_and_toc(self):
        self.append(MakeTitle())
        self.append(ClearPage())
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
        self.add_title_author_date_to_preamble()
        self.make_title_and_toc()
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
                        recipe_image = os.path.abspath(f"{self.image_path}/{recipe_file.split('.')[0]}.jpg")
                        if os.path.exists(recipe_image):
                            print(f"recipe image exists: {recipe_image}")
                            self.append(NoEscape(r"\begin{center}"))
                            self.append(NoEscape(rf"\includegraphics[scale=0.1]{{{recipe_image}}}"))
                            self.append(NoEscape(r"\end{center}"))
                            self.append(NoEscape(r"\vspace{-4em}"))
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
