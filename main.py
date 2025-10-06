from vittles.ingredient import Ingredient
from vittles.recipe import JsonRecipeImporter
from vittles.utils import RecipeAdder


test_recipe = {
    "Title": "Dorito Casserole",
    "Prep Time": "15 mins",
    "Cook Time": "35 mins",
    "Servings": "8",
    "Ingredients": [
        "1 lb lean ground beef",
        "1 yellow onion, chopped",
        "1 red bell pepper, chopped",
        "1 1oz packet taco seasoning",
        "1/2 cup water",
        "1 14.5oz can diced tomatoes and green chiles",
        "1 15oz can black beans",
        "1 cup sour cream",
        "1 9 1/4oz bag nacho cheese Doritos, crushed",
        "3 cups shredded cheddar-jack cheese",
        "1 tomato",
        "1/2 cup salsa",
    ],
    "Directions": [
        "Preheat oven to 350F. Lightly coat 3 quart baking dish with non-stick spray.",
        "Brown the ground beef, drain the grease, return to pan.",
        "Add onion and pepper and cook until tender, then add taco seasoning and water. Simmer 5 minutes.",
        "Stir in diced tomatoes, sour cream and black beans.",
        "Sprinkle bottom of baking dish with 1/3 of crushed chips. Spoon half meat mixture over chips. Top with second third of crushed chips and 1 1/2 cups cheese.",
        "Repeat with remaining meat, chips and cheese. Bake in oven for 25 minutes. Dice tomato, serve with salsa and more sour cream.",
    ],
}

# testExample = RecipeAdder(test_recipe, category="casseroles").writeToExamples()

import os
import json
from pylatex import Command, Document, Section, Subsection, Package, Enumerate, Tabular
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


class Portion(CommandBase):
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
        self.available_categories = os.listdir(self.recipe_path)
        self.available_recipes = dict()
        for category in self.available_categories:
            self.available_recipes[category.title()] = os.listdir(
                f"{self.recipe_path}/{category}"
            )

        self.preamble.append(Package("xcookybooky"))
        self.preamble.append(Package("cookingsymbols"))
        self.preamble.append(Command("title", "Vittles"))
        self.preamble.append(Command("author", "Zechariah Thurman"))
        self.preamble.append(Command("date", NoEscape(r"\today")))
        self.append(NoEscape(r"\maketitle"))
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
                        with self.create(TexIngredientsTable()):
                            with self.create(Tabular("c l")) as table:
                                for ingredient in recipe.ingredients:
                                    table.add_row(
                                        f"{ingredient.quantity} {ingredient.unit}",
                                        f"{ingredient.name}",
                                    )
                    self.append(ClearPage())


test = Vittles()
test.fill_document()
test.generate_pdf("vittles", clean_tex=False)
tex = test.dumps()
