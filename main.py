import argparse

from vittles.utils import RecipeAdder, ImageParamsAdder
from vittles import Vittles

add_recipe = {
    "Title": "Slow Cooker Pernil",
    "Prep Time": "12 hours 15 minutes",
    "Cook Time": "9 hours",
    "Servings": "8 to 10",
    "Ingredients": [
        "7-8 lb pork shoulder",
        "16 cloves garlic",
        "1 1/2 Tbs adobo seasoning",
        "1 Tbs dried oregano",
        "1/4 cup olive oil",
        "1 Tbs sofrito bouillon",
        "2 Tbs water",
        "1/2 cup water",
    ],
    "Directions": [
        "Combine garlic, adobo seasoning, oregano, 2 Tbs water and sofrito bouillon in food processor. Add olive oil to paste",
        "Make several cuts all over the pork shoulder. Slather the pork shoulder with garlic paste. Marinate 8-12 hours in fridge",
        "Place pork shoulder into slow cooker, fat side down with 1/2 cup of water. Cook for 9-10 hours on low.",
        "Shred meat into chunks with two forks",
    ],
}

# TODO: Make a util component that will autogen this
# based on the contents of json dir.
image_params = {
    "barbacoa-brisket": {
        "scale": None,
        "rotation": None,
        "following_vspace": None,
    },
    "ropa-vieja": {"scale": None, "rotation": None, "following_vspace": None},
    "easy-pulled-pork": {"scale": None, "rotation": None, "following_vspace": None},
    "dorito-casserole": {
        "scale": None,
        "rotation": None,
        "following_vspace": None,
    },
    "beef-ragu-with-warm-spices": {
        "scale": None,
        "rotation": None,
        "following_vspace": None,
    },
    "crockpot-picadillo": {
        "scale": None,
        "rotation": None,
        "following_vspace": None,
    },
    "salmar's-pork-and-mushroom-pasta": {
        "scale": None,
        "rotation": None,
        "following_vspace": None,
    },
    "slow-cooker-enchilada-quinoa": {
        "scale": None,
        "rotation": None,
        "following_vspace": None,
    },
    "title": {"scale": None, "rotation": None, "following_vspace": None},
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vittles module main script")
    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Add a recipe json file from add_recipe to json directory.",
    )
    parser.add_argument(
        "-c", "--category", default="easy", help="Category for added recipe"
    )
    parser.add_argument(
        "-v", "--vittles", action="store_true", help="Generate vittles document."
    )
    parser.add_argument(
        "-p", "--params", action="store_true", help="Generate image params."
    )

    args = parser.parse_args()

    if args.add:
        print("Adding recipe to json directory...")
        RecipeAdder(add_recipe, category=args.category).writeToJson()

    if args.params:
        print("Creating image params dict...")
        ImageParamsAdder(image_params).writeToJson()

    if args.vittles:
        print("Generating recipe book from contents of json dir...")
        recipe_book = Vittles()
        recipe_book.fill_document()
        recipe_book.generate_pdf("vittles", clean_tex=False)
        tex = recipe_book.dumps()
