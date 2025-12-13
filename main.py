import argparse

from vittles.utils import RecipeAdder, ImageParamsAdder
from vittles import Vittles

add_recipe = {
    "Title": "Black Bean and Sweet Potato Quesadillas",
    "Prep Time": "20 mins",
    "Cook Time": "1 hour",
    "Servings": "4",
    "Ingredients": [
        "1 large sweet potato",
        "1 cup salsa",
        "1 cup cooked brown rice",
        "1 cup fresh spinach",
        "1 can refried beans",
        "1 can black beans",
        "1/4 tsp onion powder",
        "1/4 tsp chili powder",
        "1/4 tsp cumin",
        "8 whole tortillas",
    ],
    "Directions": [
        "Preheat oven to 375 F. Prepare a sheet pan with parchment paper.",
        "An hour before eating, peel and chop the sweet potatoes. Bake sweet potatoes in oven for 45 minutes, until soft. While those are cooking, cook the rice.",
        "When sweet potatoes are finished, place in food processor or blender. Blend potatoes with rice, salsa and spinach.",
        "Transfer sweet potato mash into sauce pan with black and refried beans. Heat mixture over medium and add onion and chili powders and cumin.",
        "Place tortilla on griddle or frying pan at medium heat, slathering with sweet potato bean mixture. Place another tortilla on top. Cook for three minutes, then flip and cook for another three minutes.",
        "Remove from griddle or frying pan and cut into desired sections. Serve with preferred toppings.",
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
        "-c", "--category", default="slow-cooker", help="Category for added recipe"
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
