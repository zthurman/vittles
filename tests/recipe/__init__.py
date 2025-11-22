"""

vittles, recipe book generator
Copyright (C) [2025] [Zechariah Thurman]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import unittest
import json
import os
from hypothesis import given, settings, strategies as st
from fractions import Fraction

from vittles.ingredient import Ingredient
from vittles.recipe import REQUIRED_KEYS, JsonRecipeImporter


class TestRecipe(unittest.TestCase):
    def setUp(self):
        self.test_json_file = "test.json"

    def tearDown(self):
        os.remove(self.test_json_file)

    @given(
        st.fixed_dictionaries(
            mapping=dict.fromkeys(
                REQUIRED_KEYS,
                st.text(
                    alphabet=st.characters(
                        codec="latin-1",
                        min_codepoint=0x41,
                        max_codepoint=0x5A,
                    ),
                    min_size=1,
                ),
            )
        ),
    )
    def testJsonRecipeImporterRecipeValid(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)
        test = JsonRecipeImporter(self.test_json_file)
        self.assertEqual(test.recipe_valid, True)
        self.assertEqual(test.title, test_dict["Title"])
        self.assertEqual(test.preptime, test_dict["Prep Time"])
        self.assertEqual(test.cooktime, test_dict["Cook Time"])
        self.assertEqual(test.servings, test_dict["Servings"])

    @given(
        st.fixed_dictionaries(
            mapping=dict.fromkeys(
                ["Cheese", "Crackers", "Mortadella"],
                st.text(
                    alphabet=st.characters(
                        codec="latin-1",
                        min_codepoint=0x41,
                        max_codepoint=0x5A,
                    ),
                    min_size=1,
                ),
            )
        ),
    )
    def testJsonRecipeImporterRecipeInvalid(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)
        with self.assertRaises(ValueError):
            test = JsonRecipeImporter(self.test_json_file)

    @given(
        st.fixed_dictionaries(
            mapping=dict.fromkeys(
                REQUIRED_KEYS,
                st.text(
                    alphabet=st.characters(
                        codec="latin-1",
                        min_codepoint=0x41,
                        max_codepoint=0x5A,
                    ),
                    min_size=1,
                ),
            )
        ),
    )
    def testJsonRecipeImporterIngredients(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)
        test = JsonRecipeImporter(self.test_json_file)
        validation = list()
        for each in test_dict["Ingredients"]:
            validation.append(Ingredient(ingredient_str=each))
        self.assertListEqual(test.ingredients, validation)
