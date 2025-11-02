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
import os
import json
from hypothesis import given, settings, strategies as st

from vittles.recipe import REQUIRED_KEYS

from vittles.pylatex import Vittles


class TestVittles(unittest.TestCase):
    def setUp(self):
        self.test_json_file = "tests/test.json"
        self.document_validation_prefix = (
            f"\\documentclass{{article}}%\n"
            f"\\usepackage[T1]{{fontenc}}%\n"
            f"\\usepackage[utf8]{{inputenc}}%\n"
            f"\\usepackage{{lmodern}}%\n"
            f"\\usepackage{{textcomp}}%\n"
            f"\\usepackage{{lastpage}}%\n"
            f"%\n"
        )
        self.document_validation_line_ending = f"%\n"
        self.document_validation_doc_tag_prefix = (
            f"\\begin{{document}}%\n" f"\\normalsize%\n"
        )
        self.document_validation_doc_tag_suffix = f"\\end{{document}}"

    def tearDown(self):
        os.remove(self.test_json_file)

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
    def testRecipePath(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test = Vittles(recipe_path=test_recipe_dir)
        self.assertEqual(test.recipe_path, test_recipe_dir)
        self.assertEqual(
            test.recipe_path_contents, os.listdir(os.path.dirname(self.test_json_file))
        )
        self.assertEqual(len(test.available_categories), 0)
        self.assertEqual(len(test.available_recipes), 1)

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
    def testBaseDocumentSkeleton(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test = Vittles(recipe_path=test_recipe_dir)
        validation = (
            self.document_validation_prefix
            + self.document_validation_line_ending
            + self.document_validation_line_ending
            + self.document_validation_doc_tag_prefix
            + self.document_validation_doc_tag_suffix
        )
        self.assertEqual(test.dumps(), validation)

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
    def testAddPackagesToPreamble(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test = Vittles(recipe_path=test_recipe_dir)
        test.add_packages_to_preamble()
        packages_validation = (
            f"\\usepackage{{lettrine}}%\n"
            f"\\usepackage{{cookingsymbols}}%\n"
            f"\\usepackage{{xcookybooky}}%\n"
            f"%\n"
        )
        validation = (
            self.document_validation_prefix
            + packages_validation
            + self.document_validation_doc_tag_prefix
            + self.document_validation_doc_tag_suffix
        )
        self.assertEqual(test.dumps(), validation)

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
    def testAddTitleAuthorDateToPreamble(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test = Vittles(recipe_path=test_recipe_dir)
        test.add_title_author_date_to_preamble()
        title_author_date_validation = (
            f"\\title{{Vittles}}%\n"
            f"\\author{{Zam}}%\n"
            f"\\date{{\\today}}%\n"
            f"%\n"
        )
        validation = (
            self.document_validation_prefix
            + title_author_date_validation
            + self.document_validation_doc_tag_prefix
            + self.document_validation_doc_tag_suffix
        )
        self.assertEqual(test.dumps(), validation)
