from vittles.ingredient import Ingredient

from vittles.recipe import JsonRecipeImporter
from vittles.utils import RecipeAdder


test_recipe = {
    "Title": "Ropa Vieja",
    "Prep Time": "15 mins",
    "Cook Time": "4.5-7.5 hours",
    "Servings": "4 to 6",
    "Ingredients": [
        "3 Tbs vegetable oil",
        "2 onions, halved and sliced thin",
        "2 red bell peppers, stemmed, seeded, and cut into 1/2 inch wide strips",
        "1/4 cup tomato paste",
        "4 garlic cloves minced",
        "2 tsp ground cumin",
        "1 1/2 tsp dried oregano",
        "1/2 cup dry white wine",
        "2 Tbs soy sauce",
        "2 bay leaves",
        "1 (2-pound) flank steak, trimmed and cut crosswise against grain into four equal pieces",
        "3/4 cup pitted large brine-cured green olives, sliced",
        "1 Tbs distilled white vinegar",
    ],
    "Directions": [
        "Heat oil in 12-inch skillet over medium-high heat until shimmering. Add onions and peppers, cover and cook, stirring occasionally, until softened and spotty brown, 8- 10 minutes",
        "Push vegetables to side of the skillet. Add tomato paste, garlic, cumin, and oregano to center of skillet and cook, uncovered, until fragrant, about 1 minute. Stir tomato paste mixture into vegetables. Stir in wine and cook until nearly evaporated, about 2 minutes; transfer to slow cooker.",
        "Stir soy sauce and bay leaves into slow cooker. Season steak with salt and pepper and nestle cooker. Cover and cook until beef is tender and fork slips easily in and out of meat, 6 to 7 hours on low or 4 to 5 hours on high.",
        "Transfer steak to cutting board, let cool slightly, then shread into bite-size pieces using 2 forks. Discard bay leaves. Stir beef and olives into slow cooker and let sit until heated through, about 5 minutes. Stir in venegar and season with salt and pepper to taste. Serve.",
    ],
}

#testExample = RecipeAdder(test_recipe).writeToExamples()

import os
from pylatex import Command, Document, Section, Subsection, Package
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape, italic


class Recipe(Environment):
    """A class that represents an xcookybooky recipe."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RecipeBook(Document):
    def __init__(self):
        super().__init__()

        self.preamble.append(Package("xcookybooky"))
        self.preamble.append(Command("title", "Awesome Title"))
        self.preamble.append(Command("author", "Anonymous"))
        self.preamble.append(Command("date", NoEscape(r"\today")))
        self.append(NoEscape(r"\maketitle"))

    def fill_document(self):
        with self.create(Recipe()):
            self.append(NoEscape("{Test Recipe}"))

        with self.create(Section("A section")):
            self.append("Some regular text and some")
            self.append(italic("italic text"))

            with self.create(Subsection("A subsection")):
                self.append("Also some crazy characters: $&#{}")


test = RecipeBook()
test.fill_document()
test.generate_pdf("basic_testing", clean_tex=False)
tex = test.dumps()
