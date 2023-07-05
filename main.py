import mistletoe
from mistletoe.latex_renderer import LaTeXRenderer


with open("recipe.md", 'r') as recipe:
    # rendered = mistletoe.markdown(recipe)
    latex = mistletoe.markdown(recipe, LaTeXRenderer)

# print(rendered)
print(latex)
