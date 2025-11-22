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
from hypothesis import given, settings, strategies as st
from fractions import Fraction

import os
from pathlib import Path
from vittles.recipe import REQUIRED_KEYS

from vittles.utils import RecipeAdder


class TestRecipeAdder(unittest.TestCase):
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
    def testRecipeAdderNoneCategory(self, test_dict):
        test = RecipeAdder(test_dict)
        self.assertEqual(test.input_recipe, test_dict)
        self.assertEqual(test.category, None)
        test_path = Path(__file__)
        verification_path = f"{test_path.parent.parent.parent}/json/{test_dict["Title"].lower().replace(" ", "-")}.json"
        self.assertEqual(test.filename(), verification_path)
        test.writeToJson()
        self.assertTrue(
            os.path.exists(test.filename()), "The file should have been created"
        )
        os.remove(test.filename())

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
        st.text(
            alphabet=st.characters(
                codec="latin-1",
                min_codepoint=0x41,
                max_codepoint=0x5A,
            ),
            min_size=1,
        ),
    )
    def testRecipeAdderWithCategory(self, test_dict, test_category):
        test = RecipeAdder(test_dict, test_category)
        self.assertEqual(test.input_recipe, test_dict)
        self.assertEqual(test.category, test_category)
        test_path = Path(__file__)
        verification_path = f"{test_path.parent.parent.parent}/json/{test.category}/{test_dict["Title"].lower().replace(" ", "-")}.json"
        self.assertEqual(test.filename(), verification_path)
        test.writeToJson()
        self.assertTrue(
            os.path.exists(test.filename()), "The file should have been created"
        )
        os.remove(test.filename())
        os.rmdir(f"{test_path.parent.parent.parent}/json/{test.category}")
