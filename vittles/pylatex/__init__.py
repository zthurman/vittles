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
    def __init__(self, recipe_path: str = "json"):
        super().__init__()

        self.recipe_path = recipe_path
        self.available_categories = os.listdir(self.recipe_path)
        self.available_recipes = dict()
        for category in self.available_categories:
            self.available_recipes[category.title()] = os.listdir(
                f"{self.recipe_path}/{category}"
            )

        self.preamble.append(Package("lettrine"))  # for steps to show up
        self.preamble.append(Package("cookingsymbols"))
        self.preamble.append(Package("xcookybooky"))
        self.preamble.append(Title("Vittles"))
        self.preamble.append(Command("author", "Zechariah Thurman"))
        self.preamble.append(Command("date", NoEscape(r"\today")))
        self.append(MakeTitle())
        self.append(ClearPage())
        self.append(TableOfContents())
        self.append(ClearPage())

    def fill_document(self):
        for category, recipes in self.available_recipes.items():
            with self.create(Section(category)):
                for recipe_file in recipes:
                    recipe = JsonRecipeImporter(
                        input_recipe=f"{self.recipe_path}/{category.lower()}/{recipe_file}"
                    )
                    with self.create(Recipe()):
                        raw_title = rf"{{{recipe.title}}}"
                        self.append(NoEscape(raw_title))
                        self.append(
                            Portion(
                                arguments=NoEscape(
                                    rf"\Dish\enspace{{{recipe.servings}}}"
                                )
                            )
                        )
                        with self.create(Preparation()):
                            with self.create(Enumerate()) as enum:
                                for step in recipe.directions:
                                    enum.add_item(step)
                            # I don't know why Step horks the compile
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
