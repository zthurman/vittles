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
from pylatex import Document

from vittles.pylatex.extensions import (
    Title,
    MakeTitle,
    ClearPage,
    TableOfContents,
    Recipe,
    Ingredients,
    Preparation,
    Portion,
    Step,
)


class TestTitle(unittest.TestCase):
    @given(
        st.text(
            alphabet=st.characters(
                codec="latin-1", min_codepoint=0x41, max_codepoint=0x5A
            ),
            min_size=1,
        ),
    )
    def testTitle(self, title):
        test = Title(title).dumps()
        self.assertEqual(rf"\title{{{title}}}", test)


class TestMakeTitle(unittest.TestCase):
    def testMakeTitle(self):
        test = MakeTitle().dumps()
        self.assertEqual(rf"\maketitle", test)


class TestClearPage(unittest.TestCase):
    def testClearPage(self):
        test = ClearPage().dumps()
        self.assertEqual(rf"\clearpage", test)


class TestTableOfContents(unittest.TestCase):
    def testTableOfContents(self):
        test = TableOfContents().dumps()
        self.assertEqual(rf"\tableofcontents", test)


class TestRecipe(unittest.TestCase):
    @given(
        st.text(
            alphabet=st.characters(
                codec="latin-1", min_codepoint=0x41, max_codepoint=0x5A
            ),
            min_size=1,
        ),
    )
    def testRecipe(self, test_recipe):
        test = Recipe(data=test_recipe)
        test = test.dumps()
        self.assertEqual(f"\\begin{{recipe}}%\n{test_recipe}%\n\\end{{recipe}}", test)


class TestIngredients(unittest.TestCase):
    @given(
        st.text(
            alphabet=st.characters(
                codec="latin-1", min_codepoint=0x41, max_codepoint=0x5A
            ),
            min_size=1,
        ),
    )
    def testIngredients(self, test_ingredients):
        test = Ingredients(data=test_ingredients)
        test = test.dumps()
        self.assertEqual(f"\\ingredients{{%\n{test_ingredients}%\n}}", test)


class TestPreparation(unittest.TestCase):
    @given(
        st.text(
            alphabet=st.characters(
                codec="latin-1", min_codepoint=0x41, max_codepoint=0x5A
            ),
            min_size=1,
        ),
    )
    def testPreparation(self, test_preparation):
        test = Preparation(data=test_preparation)
        test = test.dumps()
        self.assertEqual(f"\\preparation{{%\n{test_preparation}%\n}}", test)


class TestPortion(unittest.TestCase):
    @given(
        st.text(
            alphabet=st.characters(
                codec="latin-1", min_codepoint=0x41, max_codepoint=0x5A
            ),
            min_size=1,
        ),
    )
    def testPortion(self, portion):
        test = Portion(arguments=portion).dumps()
        self.assertEqual(rf"\portion{{{portion}}}", test)


class TestStep(unittest.TestCase):
    @given(
        st.text(
            alphabet=st.characters(
                codec="latin-1", min_codepoint=0x41, max_codepoint=0x5A
            ),
            min_size=1,
        ),
    )
    def testStep(self, step):
        test = Step(data=step).dumps()
        self.assertEqual(f"\\step {step}", test)
