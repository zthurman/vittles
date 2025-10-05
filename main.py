from vittles.ingredient import Ingredient

# from vittles.recipe import Recipe
from vittles.utils import RecipeAdder


test_recipe = {
    "Title": "Barbacoa Brisket",
    "Prep Time": "15 mins",
    "Cook Time": "8 hours",
    "Servings": 4,
    "Ingredients": [
        "1 tsp oregano",
        "1 Tbs dark brown sugar",
        "2 Tbs olive oil",
        "1 Tbs minced chipotle chilies in adobo",
        "1 Tbs adobo sauce",
        "1 tsp ground cumin",
        "3 garlic cloves",
        "1 lbs-ish tritip",
        "2 medium tomatoes, chopped",
        "1 medium onion",
        "1 red bell pepper",
        "1 jalapeno pepper",
    ],
    "Directions": [
        "Combine first 7 ingredients in a medium bowl, stirring well to combine. Rub mixture into tritip.",
        "Arrange tomatoes, onion, bell pepper, and jalapeno in bottom of slow cooker. Place tritip on top of vegetables, and drizzle any remaining spice mixture over tritip and vegetables. Cover and cook on low for 8 hours.",
        "Remove tritip from slow cooker, and shred meat with two forks. Return tritip to slow cooker, and toss with vegetables.",
    ],
}

# testExample = RecipeAdder(test_recipe).writeToExamples()

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
