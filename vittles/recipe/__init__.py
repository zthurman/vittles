class Recipe:
    def __init__(self, input_recipe: dict):
        self.input_recipe = input_recipe
        self.recipe_valid = self.verify_input()
        assert self.recipe_valid, f"self.recipe_keys_message()"

    def recipe_keys_message(self):
        msg = f"A recipe must have: {self.required_keys()}"
        return msg

    def required_keys(self):
        return ["Title", "Ingredients", "Directions"]

    def verify_input(self):
        if all(key in self.input_recipe for key in self.required_keys()):
            return True
        else:
            return False
