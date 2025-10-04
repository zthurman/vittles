import unittest
from hypothesis import given, settings, strategies as st
from fractions import Fraction

from vittles.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    @given(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False, allow_subnormal=False),
        st.text(min_size=3, max_size=3),
        st.text(),
    )
    def testIngredientConstructor(self, i, f, unit, name):
        ingredient = f"{i} {str(Fraction(f))} {unit} {name}"
        test = Ingredient(ingredient)
        self.assertEqual(test.quantity, f"{i} {str(Fraction(f))}")
        self.assertEqual(test.unit, f"{unit}")
        self.assertEqual(test.name, f"{name}")
