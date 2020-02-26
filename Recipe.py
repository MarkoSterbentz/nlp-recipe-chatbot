import copy

class Recipe:
    '''
    Recipe
    A class for storing needed information for a single recipe and handling transformations of the recipe.
    '''
    def __init__(self, ingredients, cooking_steps):
        self.ingredients = ingredients
        self.cooking_steps = cooking_steps

    def transform_healthy(self):
        '''
        Transforms the recipe to be more healthy.
        :return: The transformed recipe.
        '''
        print('Transforming to a healthy recipe not implemented yet.')
        return Recipe(None, None)

    def transform_unhealthy(self):
        '''
        Transforms the recipe to be more unhealthy.
        :return: The transformed recipe.
        '''
        print('Transforming to an unhealthy recipe not implemented yet.')
        return Recipe(None, None)

    def transform_vegetarian(self):
        '''
        Transforms the recipe to be vegetarian.
        :return: The transformed recipe.
        '''
        # Create deep copies of the Ingredient and CookingStep lists
        new_ingredients = copy.deepcopy(self.ingredients)
        new_cooking_steps = copy.deepcopy(self.cooking_steps)

        # Identify all meat ingredients


        # For each of the meat ingredients:
            # Find the appropriate vegetarian substitution
            # Replace each reference to this meat with the replacement in the CookingSteps and Ingredient lists

        print('Transforming to a vegetarian recipe not implemented yet.')
        return Recipe(None, None)

    def transform_non_vegetarian(self):
        '''
        Transforms the recipe to be non-vegetarian.
        :return: The transformed recipe.
        '''
        print('Transforming to a non-vegetarian recipe not implemented yet.')
        return Recipe(None, None)

    def transform_Japanese(self):
        '''
        Transforms the recipe to be more Japanese.
        :return: The transformed recipe.
        '''
        print('Transforming to a Japanese recipe not implemented yet.')
        return Recipe(None, None)


    def pretty_print(self):
        '''
        Prints out the recipe in a nice format.
        :return: None
        '''

        print('***************************************************************')
        print('INGREDIENTS:')
        for ing in self.ingredients:
            ing.pretty_print()
        print('***************************************************************')
        print('COOKING STEPS:')
        for step in self.cooking_steps:
            step.pretty_print()
        print('***************************************************************')

        return

    def substitute_ingredients(self, old_ing, new_ing):
        '''
        Substitutes out the old ingredient for the new ingredient in both the ingredient list and the cooking steps.
        :param old_ing: The old ingredient to substitute out of the recipe.
        :param new_ing: The new ingredient to add to the recipe .
        :return: None
        '''
        pass
