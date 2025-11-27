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
import os
import json
from hypothesis import given, settings, strategies as st
from pylatex.utils import NoEscape

from vittles.recipe import REQUIRED_KEYS, JsonRecipeImporter

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
            f"\\title{{%\n"
            f"Vittles%\n"
            f"\\begin{{center}}%\n"
            f"\\includegraphics[angle=-90,scale=0.1]{{/home/lappy/src/vittles/img/title.jpg}}%\n"
            f"\\end{{center}}%\n"
            f"}}%\n"
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
    def testMakeTitleAndToc(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test = Vittles(recipe_path=test_recipe_dir)
        test.make_title_and_toc()
        title_and_toc_validation = (
            f"\\maketitle%\n"
            f"\\clearpage%\n"
            f"\\tableofcontents%\n"
            f"\\clearpage%\n"
        )
        validation = (
            self.document_validation_prefix
            + "%\n"
            + "%\n"
            + self.document_validation_doc_tag_prefix
            + title_and_toc_validation
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
    def testAssembleRecipeOptions(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test = Vittles(recipe_path=test_recipe_dir)
        for category, recipe_files in test.available_recipes.items():
            for recipe_file in recipe_files:
                recipe = JsonRecipeImporter(
                    input_recipe=f"{test.recipe_path}/{recipe_file}"
                )
                recipe_options = test.assemble_recipe_options(recipe)
                validation = list()
                validation.append(NoEscape(rf"portion={{{recipe.servings}}} servings"))
                validation.append(NoEscape(rf"preparationtime={{{recipe.preptime}}}"))
                validation.append(NoEscape(rf"bakingtime={{{recipe.cooktime}}}"))
                self.assertEqual(recipe_options, validation)
