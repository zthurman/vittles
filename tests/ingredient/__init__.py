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
