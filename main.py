from vittles.ingredient import Ingredient
from vittles.recipe import JsonRecipeImporter
from vittles.utils import RecipeAdder


test_recipe = {
    "Title": "Easy Pulled Pork",
    "Prep Time": "15 mins",
    "Cook Time": "4-7 hours",
    "Servings": "2 to 4",
    "Ingredients": [ "1/2 cup chicken broth",
        "2 slices bacon",
        "1 Tbs packed brown sugar",
        "1 Tbs paprika",
        "1 1/2 tsp chili powder",
        "1 lbs pork ribs",
        "3/4 cup barbecue sauce",
    ],
    "Directions": [
        "Combine broth and bacon in slow cooker. Combine sugar, paprika, chili powder in bowl. Pat ribs dry with paper towels and rub with spice mixture. Nestle ribs into slow cooker, cover and cook until pork is tender, 6-7 hours on low or 4-5 hours on high.",
        "Remove bones from ribs with tongs. Shred meat in slow cooker with two forks.",
        "Give bacon to the cat. Make a best effort to get the fat off the top of the cooking liquid. Add barbecue sauce to shredded meat and cooking liquid and mix together well.",
    ],
}

testExample = RecipeAdder(test_recipe).writeToExamples()

import os
import json
from pylatex import Command, Document, Section, Subsection, Package, Enumerate
from pylatex.base_classes import Environment, ContainerCommand, CommandBase, LatexObject
from pylatex.utils import NoEscape


class ClearPage(CommandBase):
    """A command that clears the page"""


class TableOfContents(CommandBase):
    """A command that creates a table of contents"""


class Recipe(Environment):
    """A class that represents an xcookybooky recipe."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TexIngredientsTable(ContainerCommand):
    """A class that represents xcookybooky ingredients."""

    _latex_name = "ingredients"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Preparation(ContainerCommand):
    """A class that represents xcookybooky preparation instructions."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DataOnlyCommandBase(LatexObject):
    def __init__(self, data):
        self.data = data
        super().__init()

    def dumps(self):
        """Represent the command as a string in LaTeX syntax.

        Returns
        -------
        str
            The LaTeX formatted command
        """

        return r"\{command} {data}".format(
            command=self.latex_name,
            data=self.data,
        )


class Step(DataOnlyCommandBase):
    """
    A class that represents xcookybooky step inside preparation instructions.
    This one is weird because it takes no options, arguments or extra arguments
    like the class of stuff CommandBase is built for. So we make a DataOnlyCommandBase
    above and hope for the best.
    """
    def __init__(self, data):
        super().__init__(data)


class Vittles(Document):
    def __init__(self, recipe_path: str = "json"):
        super().__init__()

        self.recipe_path = recipe_path
        self.available_recipes = os.listdir(self.recipe_path)

        self.preamble.append(Package("lettrine"))
        self.preamble.append(Package("xcookybooky"))
        self.preamble.append(Command("title", "Vittles"))
        self.preamble.append(Command("author", "Zechariah Thurman"))
        self.preamble.append(Command("date", NoEscape(r"\today")))
        self.append(NoEscape(r"\maketitle"))
        self.append(ClearPage())
        self.append(TableOfContents())
        self.append(ClearPage())

    def fill_document(self):
        with self.create(Section("Slow Cooker Meals")):
            for recipe in self.available_recipes:
                with open(f"{self.recipe_path}/{recipe}", "r") as file:
                    input_recipe = json.load(file)
                    with self.create(Recipe()):
                        raw_title = rf'{{{input_recipe["Title"]}}}'
                        self.append(NoEscape(raw_title))
                        with self.create(Preparation()):
                            with self.create(Enumerate()) as enum:
                                for step in input_recipe["Directions"]:
                                    enum.add_item(step)
                        with self.create(TexIngredientsTable()):
                            self.append(NoEscape("2 bar & Dark Chocolate"))
                self.append(ClearPage())


test = Vittles()
test.fill_document()
test.generate_pdf("basic_testing", clean_tex=False)
tex = test.dumps()
