import json
from fractions import Fraction

from vittles.ingredient import Ingredient
from vittles.recipe import Recipe

test_recipe = {
    "Title": "Barbacoa Brisket",
    "Prep Time": "",
    "Cook Time": "",
    "Servings": 8,
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
        "",
    ],
}

# Specify the filename for your JSON output
# filename = "examples/crockpot-picadillo.json"

# Open the file in write mode ('w') and use json.dump()
# with open(filename, 'w') as json_file:
#    json.dump(test_recipe, json_file, indent=4)

test = Recipe(test_recipe)
