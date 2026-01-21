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
from PIL import Image

from pylatex.utils import NoEscape

from vittles.recipe import REQUIRED_KEYS, JsonRecipeImporter

from vittles.pylatex import Vittles


class TestVittles(unittest.TestCase):
    def setUp(self):
        self.test_file_root = "tests"
        self.test_json_file = f"{self.test_file_root}/test.json"
        self.image_width = 640
        self.image_height = 480
        self.image_color = "blue"
        self.test_title_image_file = f"{self.test_file_root}/title.jpg"
        self.test_image_file = f"{self.test_file_root}/test.jpg"
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
        if os.path.exists(self.test_image_file):
            os.remove(self.test_image_file)
        if os.path.exists(self.test_title_image_file):
            os.remove(self.test_title_image_file)

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
        test_image_dir = os.path.dirname(os.path.abspath(self.test_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
        self.assertEqual(test.recipe_path, test_recipe_dir)
        self.assertEqual(
            test.recipe_path_contents,
            sorted(os.listdir(os.path.dirname(self.test_json_file))),
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
    def testImagePathForRecipeImage(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)
        test_image = Image.new(
            "RGB", (self.image_width, self.image_height), self.image_color
        )
        test_image.save(self.test_image_file)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test_image_dir = os.path.dirname(os.path.abspath(self.test_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
        self.assertEqual(test.image_path, test_image_dir)
        self.assertEqual(
            test.image_path_contents, os.listdir(os.path.dirname(self.test_image_file))
        )
        self.assertEqual(test.title_image(), None)

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
    def testImagePathForTitleImage(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)
        test_image = Image.new(
            "RGB", (self.image_width, self.image_height), self.image_color
        )
        test_image.save(self.test_title_image_file)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test_image_dir = os.path.dirname(os.path.abspath(self.test_title_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
        self.assertEqual(test.image_path, test_image_dir)
        self.assertEqual(
            test.image_path_contents,
            os.listdir(os.path.dirname(self.test_title_image_file)),
        )
        self.assertEqual(
            test.title_image(), os.path.abspath(self.test_title_image_file)
        )

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
        test_image_dir = os.path.dirname(os.path.abspath(self.test_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
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
        test_image_dir = os.path.dirname(os.path.abspath(self.test_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
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
    def testAddTitleToPreambleNoTitleImage(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=self.test_file_root)
        test.add_title_to_preamble()
        title_validation = f"\\title{{Vittles}}%\n" f"%\n"
        validation = (
            self.document_validation_prefix
            + title_validation
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
    def testAddTitleToPreambleWithTitleImage(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)
        test_image = Image.new(
            "RGB", (self.image_width, self.image_height), self.image_color
        )
        test_image.save(self.test_title_image_file)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=self.test_file_root)
        test.add_title_to_preamble()
        title_validation = (
            f"\\title{{%\n"
            f"Vittles%\n"
            f"\\begin{{center}}%\n"
            f"\\includegraphics[scale=0.1]{{{os.path.abspath(self.test_title_image_file)}}}%\n"
            f"\\end{{center}}%\n"
            f"}}%\n"
            f"%\n"
        )
        validation = (
            self.document_validation_prefix
            + title_validation
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
    def testAddAuthorToPreamble(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test_image_dir = os.path.dirname(os.path.abspath(self.test_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
        test.add_author_to_preamble()
        author_validation = f"\\author{{Zam}}%\n" f"%\n"
        validation = (
            self.document_validation_prefix
            + author_validation
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
    def testAddDateToPreamble(self, test_dict):
        with open(self.test_json_file, "w") as test_file:
            json.dump(test_dict, test_file, indent=4)

        test_recipe_dir = os.path.dirname(os.path.abspath(self.test_json_file))
        test_image_dir = os.path.dirname(os.path.abspath(self.test_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
        test.add_date_to_preamble()
        date_validation = f"\\date{{\\today}}%\n" f"%\n"
        validation = (
            self.document_validation_prefix
            + date_validation
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
        test_image_dir = os.path.dirname(os.path.abspath(self.test_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
        test.make_title()
        test.make_toc()
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
        test_image_dir = os.path.dirname(os.path.abspath(self.test_image_file))
        test = Vittles(recipe_path=test_recipe_dir, image_path=test_image_dir)
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
