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
    def __init__(self, data):
        self.data = data
        super().__init()

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
    like the class of stuff CommandBase is built for. So we make a DataOnlyCommandBase
    above and hope for the best.
    """

    def __init__(self, data):
        super().__init__(data)
