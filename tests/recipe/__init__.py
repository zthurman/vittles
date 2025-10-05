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
import json
import os
from hypothesis import given, settings, strategies as st
from fractions import Fraction

from vittles.recipe import REQUIRED_KEYS, JsonRecipeImporter


class TestRecipe(unittest.TestCase):
    def setUp(self):
        self.test_json_file = "test.json"

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
    def testJsonRecipeImporter(self, dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(dict, test_file, indent=4)
        test = JsonRecipeImporter(self.test_json_file)
        self.assertEqual(test.recipe_valid, True)
        os.remove(self.test_json_file)
