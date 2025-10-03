import json
from fractions import Fraction


class Ingredient:
    def __init__(self, ingredient_str: str):
        self._ingredient = ingredient_str.split()
        self.quantity = " ".join(self.quantity_finder())
        # We'll assume that after we've nuked all
        # the quantity info, the thing immediately
        # after will be the unit.
        self.unit = self._ingredient[0]
        # And everything after that is the name
        self.name = " ".join(self._ingredient[1:])

    def quantity_finder(self):
        quantity_items = list()
        # tricky list copy syntax, so we can
        # poop things off when we determine
        # they're part of the quantity info
        for each in self._ingredient[:]:
            try:
                # If the first character of the
                # string is a number we hope it's
                # part of the ingredient quantity
                # But if it ends in a % its probably
	        # a pesky ground beef grade hiding
	        # at the back of the number so bail
	        # early if that happens
                if each[-1] == "%":
                    continue
                int(each[0])
                quantity_items.append(each)
                self._ingredient.remove(each)
            except:
                # They say that this is an anti-pattern,
                # but in this case it's justified
                # MUAHAHAHAHAHAHAHA
                pass
        return quantity_items


ingredient = "3/4 tsp brown gravy"
test = Ingredient(ingredient)
print(test.quantity)
print(test.unit)
print(test.name)

ingredient = "1 3/4 cup brown gravy"
test = Ingredient(ingredient)
print(test.quantity)
print(test.unit)
print(test.name)


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


class Recipe:
    def __init__(self, input_recipe: dict):
        self.input_recipe = input_recipe
        self.recipe_valid = self.verify_input()
        assert self.recipe_valid, f"self.recipe_keys_message()"

    def recipe_keys_message(self):
        msg = f"A recipe must have: {self.required_keys()}"
        return msg

    def required_keys(self):
        return ["Title", "Ingredients", "Directions"]

    def verify_input(self):
        if all(key in self.input_recipe for key in self.required_keys()):
            return True
        else:
            return False


test = Recipe(test_recipe)
