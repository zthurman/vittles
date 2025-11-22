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
