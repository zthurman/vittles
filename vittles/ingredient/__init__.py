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


def is_within_code_points(s, min_code, max_code):
    return all(min_code <= ord(c) <= max_code for c in s)


class Ingredient:
    def __init__(self, ingredient_str: str):
        self._ingredient = ingredient_str.split()
        self.quantity = " ".join(self.quantity_finder())
        # We'll assume that after we've nuked all
        # the quantity info, the thing immediately
        # after will be the unit.
        assert is_within_code_points(
            self._ingredient[0], 0x41, 0x5A
        ) or is_within_code_points(
            self._ingredient[0], 0x61, 0x7A
        ), f"What kind of unit is this: {self_ingredient[0]}?"
        self.unit = self._ingredient[0]
        # And everything after that is the name
        self.name = " ".join(self._ingredient[1:])

    def quantity_finder(self):
        quantity_items = list()
        # tricky list copy syntax, so we can
        # poop things off when we determine
        # they're part of the quantity info
        for each in self._ingredient[:]:
            try:
                # If the first character of the
                # string is a number we hope it's
                # part of the ingredient quantity
                # But if it ends in a % its probably
                # a pesky ground beef grade hiding
                # at the back of the number so bail
                # early if that happens
                if each[-1] == "%":
                    continue
                int(each[0])
                quantity_items.append(each)
                self._ingredient.remove(each)
            except:
                # They say that this is an anti-pattern,
                # but in this case it's justified
                # MUAHAHAHAHAHAHAHA
                pass
        return quantity_items
