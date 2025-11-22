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

from pylatex.base_classes import Environment, ContainerCommand, CommandBase, LatexObject


# General LaTeX Extensions


class Title(CommandBase):
    """A command that adds the title"""


class MakeTitle(CommandBase):
    """A command that actually generates the title"""


class ClearPage(CommandBase):
    """A command that clears the page"""


class TableOfContents(CommandBase):
    """A command that creates a table of contents"""


# xcookybooky Specific LaTeX Extensions


class Recipe(Environment):
    """A class that represents an xcookybooky recipe."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Ingredients(ContainerCommand):
    """A class that represents xcookybooky ingredients."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Preparation(ContainerCommand):
    """A class that represents xcookybooky preparation instructions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Portion(CommandBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DataOnlyCommandBase(LatexObject):
    def __init__(self, *, data=None):
        self.data = data
        super().__init__()

    def dumps(self):
        """Represent the command as a string in LaTeX syntax.

        Returns
        -------
        str
            The LaTeX formatted command
        """

        return r"\{command} {data}".format(
            command=self.latex_name,
            data=self.data,
        )


class Step(DataOnlyCommandBase):
    """
    A class that represents xcookybooky step inside preparation instructions.
    This one is weird because it takes no options, arguments or extra arguments
    like the class of commands that CommandBase is built for. So we make a
    DataOnlyCommandBase above to cover us.
    """

    def __init__(self, *, data=None):
        super().__init__(data=data)
