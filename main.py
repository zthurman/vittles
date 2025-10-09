import argparse

from vittles.utils import RecipeAdder
from vittles import Vittles

add_recipe = {
    "Title": "Slow Cooker Enchilada Quinoa",
    "Prep Time": "15 mins",
    "Cook Time": "4-7 hours",
    "Servings": "4",
    "Ingredients": [
        "1 15oz can black beans",
        "1 15oz can yellow corn",
        "2 15oz cans red enchilada sauce",
        "1 15oz can fire roasted tomatoes and green chiles",
        "1 cup uncooked quinoa",
        "1/2 cup water",
        "4 oz cream cheese",
        "1 12 oz ball of oaxaca cheese, shredded",
    ],
    "Directions": [
        "Add beans, corn, 1 can of enchilada sauce, dice tomatoes and chiles, quinoa, water, and cubed cream cheese to the slow cooker. Stir everything together."
        "Pour remaining can of enchilada sauce on top, then cover with the shredded cheese. Cover and cook 4-5 hours on high or 5-7 hours on low."
        "Uncover and top with favorite toppings."
    ],
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vittles module main script")
    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Add a recipe json file from add_recipe to json directory.",
    )
    parser.add_argument("-c", "--category", default="slow-cooker", help="Category for added recipe")
    parser.add_argument(
        "-v", "--vittles", action="store_true", help="Generate vittles document."
    )

    args = parser.parse_args()

    if args.add:
        print("Adding recipe to json...")
        RecipeAdder(add_recipe, category=args.category).writeToExamples()

    if args.vittles:
        print("Generating recipe book from contents of json dir...")
        recipe_book = Vittles()
        recipe_book.fill_document()
        recipe_book.generate_pdf("vittles", clean_tex=False)
        tex = recipe_book.dumps()
