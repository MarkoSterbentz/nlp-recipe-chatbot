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


    def __str__(self):
        '''
        Prints out the recipe in a nice format.
        :return: None
        '''
        ret_val = ''
        ret_val += '***************************************************************\n'
        ret_val += 'INGREDIENTS:\n'
        ret_val += '\n'.join([str(ingredient) for ingredient in self.ingredients]) + '\n'
        ret_val += '*************\n**************************************************'
        ret_val += 'COOKING STEPS:\n'
        ret_val += '\n'.join([str(cooking_step) for cooking_step in self.cooking_steps]) + '\n'
        ret_val += '***************************************************************\n'

        return ret_val

