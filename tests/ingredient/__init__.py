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
import re
from hypothesis import given, settings, strategies as st
from fractions import Fraction

from vittles.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    @given(
        st.integers(min_value=1),
        st.floats(
            min_value=0.1,
            max_value=0.99,
            allow_nan=False,
            allow_infinity=False,
            allow_subnormal=False,
        ),
        st.text(
            alphabet=st.characters(
                codec="latin-1", min_codepoint=0x41, max_codepoint=0x5A
            ),
            min_size=1,
        ),
        st.text(
            alphabet=st.characters(
                codec="latin-1", min_codepoint=0x41, max_codepoint=0x5A
            ),
            min_size=1,
        ),
    )
    def testIngredientConstructor(self, i, f, unit, name):
        ingredient = f"{i} {str(Fraction(f))} {unit} {name}"
        test = Ingredient(ingredient)
        self.assertEqual(test.quantity, f"{i} {str(Fraction(f))}")
        self.assertEqual(test.unit, f"{unit}")
        self.assertEqual(test.name, f"{name}")
