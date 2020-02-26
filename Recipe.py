import copy
from substitutions import SUB
import random

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
        :return: The transformed recipe. A dictionary mapping original ingredients to their substitution/scaled version.
        '''

        # Make a copy of the current recipe
        transformed_recipe = Recipe(copy.deepcopy(self.ingredients), copy.deepcopy(self.cooking_steps))

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['to_healthy']:

                # Pick a new ingredient to substitute in
                new_ing_name = random.choice(SUB['to_healthy'][orig_ing.name])

                # Perform the ingredient substitution
                transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                # make a note of which ingredient was substituted for what (so we can report that to the user)
                actual_substitutions[orig_ing.name] = new_ing_name

        # If no whole ingredient substitutions were made, half the amount of condiments or unhealthy spices/herbs
        if len(actual_substitutions) == 0:
            # TODO: Implement a way to find unhealthy spices/herbs in the recipe and half the amount of them
            pass

        return transformed_recipe, actual_substitutions

    def transform_unhealthy(self):
        '''
        Transforms the recipe to be more unhealthy.
        :return: The transformed recipe.
        '''
        # Make a copy of the current recipe
        transformed_recipe = Recipe(copy.deepcopy(self.ingredients), copy.deepcopy(self.cooking_steps))

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['to_unhealthy']:

                # Pick a new ingredient to substitute in
                new_ing_name = random.choice(SUB['to_unhealthy'][orig_ing.name])

                # Perform the ingredient substitution
                transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                # make a note of which ingredient was substituted for what (so we can report that to the user)
                actual_substitutions[orig_ing.name] = new_ing_name

        # If no whole ingredient substitutions were made, half the amount of condiments or unhealthy spices/herbs
        if len(actual_substitutions) == 0:
            # TODO: Implement a way to find unhealthy spices/herbs in the recipe and double the amount of them
            pass

        return transformed_recipe, actual_substitutions

    def transform_vegetarian(self):
        '''
        Transforms the recipe to be vegetarian.
        :return: The transformed recipe.
        '''

        # Make a copy of the current recipe
        transformed_recipe = Recipe(copy.deepcopy(self.ingredients), copy.deepcopy(self.cooking_steps))

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['to_vegetarian']:

                # Pick a new ingredient to substitute in
                new_ing_name = random.choice(SUB['to_vegetarian'][orig_ing.name])

                # Perform the ingredient substitution
                transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                # make a note of which ingredient was substituted for what (so we can report that to the user)
                actual_substitutions[orig_ing.name] = new_ing_name

        return transformed_recipe, actual_substitutions


    def transform_non_vegetarian(self):
        '''
        Transforms the recipe to be non-vegetarian.
        :return: The transformed recipe.
        '''
        # Make a copy of the current recipe
        transformed_recipe = Recipe(copy.deepcopy(self.ingredients), copy.deepcopy(self.cooking_steps))

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['to_non_vegetarian']:

                # Pick a new ingredient to substitute in
                new_ing_name = random.choice(SUB['to_non_vegetarian'][orig_ing.name])

                # Perform the ingredient substitution
                transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                # make a note of which ingredient was substituted for what (so we can report that to the user)
                actual_substitutions[orig_ing.name] = new_ing_name

        return transformed_recipe, actual_substitutions

    def transform_Japanese(self):
        '''
        Transforms the recipe to be more Japanese.
        :return: The transformed recipe.
        '''
        # Make a copy of the current recipe
        transformed_recipe = Recipe(copy.deepcopy(self.ingredients), copy.deepcopy(self.cooking_steps))

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['japan']:

                # Pick a new ingredient to substitute in
                new_ing_name = random.choice(SUB['japan'][orig_ing.name])

                # Perform the ingredient substitution
                transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                # make a note of which ingredient was substituted for what (so we can report that to the user)
                actual_substitutions[orig_ing.name] = new_ing_name

        return transformed_recipe, actual_substitutions


    def __str__(self):
        '''
        Prints out the recipe in a nice format.
        :return: None
        '''
        ret_val = ''
        ret_val += '***************************************************************\n'
        ret_val += 'INGREDIENTS:\n'
        ret_val += '\n'.join([str(ingredient) for ingredient in self.ingredients]) + '\n'
        ret_val += '***************************************************************'
        ret_val += 'COOKING STEPS:\n'
        ret_val += '\n'.join([str(cooking_step) for cooking_step in self.cooking_steps]) + '\n'
        ret_val += '***************************************************************\n'

        return ret_val

    def substitute_ingredients(self, old_ing, new_ing_name):
        '''
        Substitutes out the old ingredient for the new ingredient in both the ingredient list and the cooking steps.
        :param old_ing: The old ingredient to substitute out of the recipe.
        :param new_ing_name: The name new ingredient to add to the recipe .
        :return: None
        '''
        # TODO: Implement this function
        pass
