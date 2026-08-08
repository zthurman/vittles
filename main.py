import argparse

from vittles.utils import RecipeAdder, ImageParamsAdder
from vittles import Vittles

add_recipe = {
    "Title": "Goan Fish Surprise",
    "Prep Time": "45 minutes",
    "Cook Time": "6 hours",
    "Servings": "8 to 10",
    "Ingredients": [
        "1 yellow onion",
        "4 garlic cloves",
        "2-3 Tbsp Goan Fish spice blend (World Market Curry Festival Blend)",
        "1 14 oz can diced tomatoes",
        "2 Tbsp tomato paste",
        "1 cup dried green lentils",
        "8 oz white button mushrooms",
        "2 cups vegetable broth",
        "1 14oz can full-fat coconut cream",
        "1 15oz can great northern beans",
        "8 oz paneer",
        "8 oz extra firm tofu",
    ],
    "Directions": [
        "Add tomatoes, paste, rinsed dried lentils, sliced mushrooms, diced onion, minced garlic, vegetable broth and Goan Fish spice blend to crock pot, stir to mix.",
        "Cook on low for 4-5 hours.",
        "During last hour of slow cook, add coconut cream and northern beans to crock pot. After that, fry paneer and pressed extra firm tofu in avocado oil on a griddle.",
        "During last 20 minutes of slow cook, add fried tofu and paneer to the crock pot.",
        "The surprise is that there's no fish in it.",
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
