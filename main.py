import argparse

from vittles.utils import RecipeAdder
from vittles import Vittles

add_recipe = {
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vittles module main script")
    parser.add_argument('-a', '--add', action='store_true', help='Add a recipe json file from add_recipe to json directory.')
    parser.add_argument('-v', '--vittles', action='store_true', help='Generate vittles document.')

    args = parser.parse_args()

    if args.add:
        print("Adding recipe to json...")
        RecipeAdder(add_recipe, category="casseroles").writeToExamples()

    if args.vittles:
        print("Generating recipe book from contents of json dir...")
        recipe_book = Vittles()
        recipe_book.fill_document()
        recipe_book.generate_pdf("vittles", clean_tex=False)
        tex = recipe_book.dumps()
