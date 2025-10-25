"""

Copyright [2025] [Zechariah Thurman]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

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
