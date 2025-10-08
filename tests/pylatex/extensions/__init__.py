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
