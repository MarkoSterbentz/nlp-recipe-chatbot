import RecipeParser.RecipeParser as rp
import string
import sys

class InterfaceManager:
    '''
    Interface Manager
    Manages user interaction with the recipe transformer.
    '''

    def __init__(self, current_recipe=None, current_recipe_step=None, waiting_for_answer=False, last_question=None, terminate=False):
        self.current_recipe = current_recipe            # Recipe object denoting the recipe the user is trying to make
        self.current_recipe_step = current_recipe_step  # Integer denoting the current step in the recipe the user is on
        self.waiting_for_answer = waiting_for_answer    # Boolean denoting whether the bot is waiting for an answer to a question it asked the user
        self.last_question = last_question              # String denoting the type of the most recent question the bot asked the user
        self.terminate = terminate                      # Boolean denoting whether the conversation should end

    def start_interaction_loop(self):
        '''
        The main loop that handles all user interaction with the user.
        :return: None
        TODO: Delete this function since the interaction is all handled through Rasa.
        '''

        # Print an initial welcome message
        print('Hi! I\'m Remy! Are you ready to cook?')
        self.waiting_for_answer = True
        self.last_question = 'get_recipe'

        while not self.terminate:
            # Parse the input
            user_input = input()

            # Determine the intent of the input and the action to be taken
            action_string, arg = self.determine_intent(user_input.lower())

            # Perform the action
            if action_string == 'get_recipe':
                self.action_get_recipe()
            elif action_string == 'display_ingredient_list':
                self.action_display_ingredient_list()
            elif action_string == 'display_current_step':
                self.action_display_current_step()
            elif action_string == 'go_to_step':
                self.action_go_to_step(arg)
            elif action_string == 'answer_how_to':
                self.action_answer_how_to(arg)
            elif action_string == 'answer_what_is':
                self.action_answer_what_is(arg)
            elif action_string == 'terminate':
                self.terminate = True
            else:
                # Don't know what they're saying.
                print('Sorry, I didn\'t catch that. Could you try rephrasing that?')

        print('Thanks for talking with me today! I hope you enjoy your meal!')

        return

    def determine_intent(self, s):
        '''
        Determines the user's intent in a given string and returns the proper action to be taken.
        :param s: The string of user input.
        :return: The action to be taken based on the intent detected in the string, as well as the argument required for
        that action to be done properly.
        TODO: Delete this function, since the intent handling is done within Rasa.
        '''
        if s == 'quit':
            return 'terminate', None
        elif 'show' in s:
            if 'ingredient' in s:
                return 'display_ingredient_list', None
            elif 'step' in s:
                return 'display_current_step', None
            else:
                return None, None
        elif 'what is' in s:
            return 'answer_what_is', s.replace('what is', '')
        elif 'how' in s:
            return 'answer_how_to', s.replace('how', '')
        elif 'go to step' in s:
            return 'go_to_step', s.split().pop()
        elif self.waiting_for_answer:
            if 'yes' in s and self.last_question == 'get_recipe':
                return 'get_recipe', None
            elif self.last_question == 'view_recipe':
                if '1' in s:
                    return 'display_ingredient_list', None
                elif '2' in s:
                    return 'display_current_step', None
                else:
                    return None, None
        else:
            return None, None

    def action_get_recipe(self, url):
        '''
        Asks the user for a recipe URL from AllRecipes.com.
        :return: Returns Boolean denoting whether the recipe getting was a success or not.
        '''

        # url = input('Alrighty, give me a recipe from AllRecipes.com: ')

        # Initialize a Recipe object based on this recipe
        self.current_recipe = rp.get_recipe(url)

        if self.current_recipe is None:
            return False
        else:
            return True

    def action_display_ingredient_list(self):
        '''
        Displays the ingredient list of the current recipe.
        :return: The ingredients string,.
        '''
        return self.current_recipe.get_ingredients_string()

    def action_display_all_steps(self):
        '''
        Displays all of the cooking steps in the current recipe.
        :return: The cooking steps string.
        '''
        # self.waiting_for_answer = False
        return self.current_recipe.get_cooking_steps_string()

    def action_display_current_step(self):
        '''
        Displays the cooking step the user is currently working on.
        :return: The string with the current cooking step.
        Note: Assumes that the values in self.current_recipe_step is within the appropriate range
        '''
        ret_val = ""
        if self.current_recipe_step is not None and 0 <= self.current_recipe_step < len(self.current_recipe.cooking_steps):
            ret_val += 'Step ' + str(self.current_recipe_step + 1) + '. ' + str(self.current_recipe.cooking_steps[self.current_recipe_step]) + '\n'
        return ret_val

    def action_go_to_step(self, n):
        '''
        Displays the nth step of the current recipe, if it exists.
        :param n: The int containing the step to go to.
        :return: Boolean values saying whether the recipe state was updated properly.
        '''
        try:
            # Go to the proper cooking step
            if n < 0:
                self.current_recipe_step = 0
            elif n > len(self.current_recipe.cooking_steps) - 1:
                self.current_recipe_step = len(self.current_recipe.cooking_steps) - 1
            else:
                self.current_recipe_step = n

            # # Display the current step
            step_text = self.action_display_current_step()

            success = True
        except:
            success = False
            step_text = None

        return success, step_text

    def action_go_to_first_step(self):
        '''
        Wrapper for the function action_got_step() that goes to the first step in the current recipe.
        :return: Same as the return values for action_go_to_step().
        '''
        return self.action_go_to_step(0)

    def action_go_to_last_step(self):
        '''
        Wrapper for the function action_go_to_step() that goes to the last possible step in the recipe.
        :return: Same as the return values for action_go_to_step().
        '''
        return self.action_go_to_step(sys.maxsize)

    def action_go_to_next_step(self):
        '''
        Wrapper for the function action_go_to_step() that goes to the next possible step in the recipe.
        :return: Same as the return values for action_go_to_step().
        '''
        n = min(self.current_recipe_step + 1, len(self.current_recipe.cooking_steps) - 1)
        return self.action_go_to_step(n)

    def action_answer_how_to(self, action):
        '''
        Displays the search results from YouTube for 'how to <action>?'
        :param action: The action to search Youtube how to do.
        Note: Queries on YouTube have the form: https://www.youtube.com/results?search_query=how+to+<action>
        :return: None
        '''
        s = 'That\'s a good question! Here are some results I found for that: '
        s += 'https://www.youtube.com/results?search_query=how+to+'
        s += '+'.join(self.__remove_punctuation(action).split())
        return s

    def action_answer_what_is(self, thing):
        '''
        Displays the search results from Google for 'what is <thing>?'
        :param thing: The string of the thing to search Google for what it is.
        Note: Queries on Google have the form: https://www.google.com/search?q=what+is+<thing>
        :return: None
        '''
        s = 'That\'s a good question! Here are some results I found for that: '
        s += 'https://www.google.com/search?q=what+is+'
        s += '+'.join(self.__remove_punctuation(thing).split())
        return s

    def action_transform_recipe(self, transformation):
        '''
        Updates the recipe with the provided transformation.
        :param transformation: A string denoting the type of transformation from Project 2.
        :return: None
        Note: The transformation parameter is expected to have one of the following values:
                - healthy
                - unhealthy
                - vegetarian
                - non-vegetarian
                - japanese
                - mexican
                - italian
                - double
                - half
        '''
        # TODO: Should this print out the result of the transformation as in the last project?
        # TODO: Should this print/do anything out if it doesn't recognize the provided transformation string?
        substitutions_performed = None
        if self.current_recipe is not None:
            if transformation == 'healthy':
                self.current_recipe, substitutions_performed = self.current_recipe.transform_healthy()
            elif transformation == 'unhealthy':
                self.current_recipe, substitutions_performed = self.current_recipe.transform_unhealthy()
            elif transformation == 'vegetarian':
                self.current_recipe, substitutions_performed = self.current_recipe.transform_vegetarian()
            elif transformation == 'non-vegetarian':
                self.current_recipe, substitutions_performed = self.current_recipe.transform_non_vegetarian()
            elif transformation == 'japanese':
                self.current_recipe, substitutions_performed = self.current_recipe.transform_cuisine('japan')
            elif transformation == 'mexican':
                self.current_recipe, substitutions_performed = self.current_recipe.transform_cuisine('mexico')
            elif transformation == 'italian':
                self.current_recipe, substitutions_performed = self.current_recipe.transform_cuisine('italy')
            elif transformation == 'double':
                self.current_recipe = self.current_recipe.transform_size(2.0)
            elif transformation == 'half':
                self.current_recipe = self.current_recipe.transform_size(0.5)
        return self.action_get_substitutions_performed_string(substitutions_performed)

    def action_get_transformation_options(self):
        '''
        Builds a string containing the transformation options.
        :return: A nicely formatted string containing the transformation options.
        '''
        s = ''
        s += '\n***************************************************************\n'
        s += 'Recipe Transformation Options:\n'
        s += '[0]: Make recipe healthy\n'
        s += '[1]: Make recipe unhealthy\n'
        s += '[2]: Make recipe vegetarian\n'
        s += '[3]: Make recipe non-vegetarian\n'
        s += '[4]: Make recipe Japanese\n'
        s += '[5]: Make recipe Mexican\n'
        s += '[6]: Make recipe Italian\n'
        s += '[7]: Make recipe double portion\n'
        s += '[8]: Make recipe half portion\n'
        s += '[9]: End session\n'
        s += '***************************************************************\n'
        return s

    def action_get_substitutions_performed_string(self, subs):
        '''
        Builds a string out of the substitution dictionary.
        :param subs: A dictionary mapping the name of the original ingredient to the name of the new ingredient.
        :return: A nicely formatted string for displaying the substitutions performed.
        '''
        if subs is not None:
            s = ''
            s += '\n***************************************************************\n'
            s += 'SUBSTITUTIONS PERFORMED\n'
            s += '***************************************************************\n'
            for key, value in subs.items():
                s += key + ' -> ' + value + '\n'
            return s
        else:
            return None

    def __remove_punctuation(self, s):
        '''
        Remove all punctuation from the given string.
        :param s: The original string.
        :return: The original string without any punctuation.
        '''
        return s.translate(str.maketrans('', '', string.punctuation))
