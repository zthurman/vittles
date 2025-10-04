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

from vittles.recipe import REQUIRED_KEYS, Recipe


class TestRecipe(unittest.TestCase):
    @given(
        st.dictionaries(keys=st.sampled_from(REQUIRED_KEYS), values=st.text()),
    )
    def testRecipeConstructor(
        self, dict
    ):
        pass
