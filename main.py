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

