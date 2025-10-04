import unittest
import re
from hypothesis import given, settings, strategies as st
from fractions import Fraction

from vittles.recipe import Recipe


class TestRecipe(unittest.TestCase):
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
    def testRecipeConstructor(self, i, f, unit, name):
        pass
