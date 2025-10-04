import unittest

from vittles.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    def testIngredientBrownGravy(self):
        ingredient = "3/4 tsp brown gravy"
        test = Ingredient(ingredient)
        self.assertEqual(test.quantity, "3/4")
        self.assertEqual(test.unit, "tsp")
        self.assertEqual(test.name, "brown gravy")

    def testIngredientPintoBeans(self):
        ingredient = "1 1/3 cup pinto beans"
        test = Ingredient(ingredient)
        self.assertEqual(test.quantity, "1 1/3")
        self.assertEqual(test.unit, "cup")
        self.assertEqual(test.name, "pinto beans")
