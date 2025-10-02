import json
from fractions import Fraction


class Ingredient:
	def __init__(self, ingredient_str: str):
		self._ingredient = ingredient_str.split()
		self.quantity = float(Fraction(self._ingredient[0]))
		self.unit = self._ingredient[1]
		self.name = " ".join(self._ingredient[2:])


ingredient = "3/4 tsp brown gravy"
test = Ingredient(ingredient)
print(test.quantity)
print(test.unit)
print(test.name)

test_recipe = {
	"Title" : "Crock Pot Picadillo",
	"Prep Time" : "15 mins",
	"Cook Time" : "3 hours 12 mins",
	"Servings" : 11,
	"Ingredients" : [
		"2 1/2 lbs 93% lean ground beef",
		"1 cup minced onion",
		"1 cup diced red bell peppers",
		"3 cloves garlic",
		"1/4 cup minced cilantro",
		"1 small tomato, diced",
		"8 oz can tomato sauce",
		"1/4 cup olives",
		"1 1/2 tsp ground cumin",
		"1/4 tsp garlic powder",
		"2 bay leaves",
		"1 1/4 cups water",
	],
	"Directions" : [
		"Brown meat in a large skillet on medium-high heat. Use a wooden spoon to break the meat up into small pieces.",
		"When meat is no longer pink, drain all the liquid from pan. Add the onions, garlic and bell peppers to the meat and cook an addiotional 3-4 minutes.",
		"Transfer the meat to the slow cooker, then add tomato, cilantro, tomato sauce, water, olives (with some of the brine), then add the spices",
		"Set slow cooker to HIGH for 3-4 hours or LOW for 6-8 hours."
	]
}

# Specify the filename for your JSON output
#filename = "examples/crockpot-picadillo.json"

# Open the file in write mode ('w') and use json.dump()
#with open(filename, 'w') as json_file:
#    json.dump(test_recipe, json_file, indent=4) 

class Recipe:
	def __init__(self, input_recipe: dict):
		self.input_recipe = input_recipe
		self.recipe_valid = self.verify_input()
		assert self.recipe_valid, f"Recipe must have: {self.required_keys()}"

	def required_keys(self):
		return ["Title", "Ingredients", "Directions"]

	def verify_input(self):
		if all(key in self.input_recipe for key in self.required_keys()):
			return True
		else:
			return False

test = Recipe(test_recipe)
