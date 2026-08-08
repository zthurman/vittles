import argparse

from vittles.utils import RecipeAdder, ImageParamsAdder
from vittles import Vittles

add_recipe = {
    "Title": "Turkey Sloppy Joes",
    "Prep Time": "15 minutes",
    "Cook Time": "30 minutes",
    "Servings": "6",
    "Ingredients": [
        "1 Tbsp vegetable oil",
        "1 lb ground turkey",
        "1/2 large yellow onion",
        "1/2 green bell pepper",
        "1/2 tsp chili powder",
        "1/2 tsp garlic powder",
        "1 Tbsp stone ground mustard",
        "1/2 cup ketchup",
        "1/3 cup barbecue sauce",
        "3 Tbsp tomato paste",
        "1 Tbsp brown sugar",
        "1 Tbsp apple cider vinegar",
        "1 tsp Worcestershire sauce",
        "1/2 cup water",
    ],
    "Directions": [
        "Toast buns, in a skillet heated to medium high add vegetable oil. Add buns, cut side down. Cook until golden brown. Remove to wire rack.",
        "Add turkey, diced onion, and diced bell pepper to skillet. Cook until turkey is cooked through.",
        "Reduce to low heat. Add chili powder, mustard, garlic powder, ketchup, barbecue sauce, tomato paste, sugar, vinegar, Worcestershire sauce and water. Stir well to combine.",
        "Simmer for 10-15 minutes until sauce is at desired thickness.",
        "Add to buns with any desired toppings and serve.",
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
