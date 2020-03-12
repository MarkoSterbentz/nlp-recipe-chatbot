import RecipeParser as rp
import string

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
        TODO: This is (I think) where RASA will be deployed.
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

    def action_get_recipe(self):
        '''
        Asks the user for a recipe URL from AllRecipes.com.
        :return: Returns the recipe object, if it was a valid URL
        '''

        while self.current_recipe is None:
            url = input('Alrighty, give me a recipe from AllRecipes.com: ')

            # Initialize a Recipe object based on this recipe
            self.current_recipe = rp.get_recipe(url)

            if self.current_recipe is None:
                print('Sorry, I wasn\'t able to find a recipe there.\n')

            print('Sounds good! I was able to find a recipe for \'{}\'. What would you like to do?'.format(self.current_recipe.title))
            print('[1] See the ingredient list or [2] View the steps?')
            self.last_question = 'view_recipe'
            self.waiting_for_answer = True
            self.current_recipe_step = 0


    def action_display_ingredient_list(self):
        '''
        Displays the ingredient list of the current recipe.
        :return: None
        '''
        print(self.current_recipe.get_ingredients_string())
        print('There you go! Let me know how else I can help.')
        self.waiting_for_answer = False

        return

    def action_display_all_steps(self):
        '''
        Displays all of the cooking steps in the current recipe.
        :return: None
        Note: I'm not sure we'll ever use this.
        '''
        print(self.current_recipe.get_cooking_steps_string())
        print('There you go! Let me know how else I can help.')
        self.waiting_for_answer = False
        return

    def action_display_current_step(self):
        '''
        Displays the cooking step the user is currently working on.
        :return: None
        Note: Assumes that the values in self.current_recipe_step is within the appropriate range
        '''
        if self.current_recipe_step is not None and 0 <= self.current_recipe_step < len(self.current_recipe.cooking_steps):
            print('Step ' + str(self.current_recipe_step) + '. ' + str(self.current_recipe.cooking_steps[self.current_recipe_step]) + '\n')
        print('There you go! Let me know how else I can help.')
        self.waiting_for_answer = False
        return

    def action_go_to_step(self, arg):
        '''
        Displays the nth step of the current recipe, if it exists.
        :param arg: The string containing the step to go to.
        :return: None
        '''
        # TODO: Determine what step the user is asking for based on the arg and the current_recipe_step
        # TODO: This currently assumes that the navigational utterance is of the form 'go to step n'
        try:
            n = int(arg)

            # Go to the proper cooking step
            if n < 0:
                self.current_recipe_step = 0
            elif n > len(self.current_recipe.cooking_steps):
                self.current_recipe_step = len(self.current_recipe.cooking_steps) - 1
            else:
                self.current_recipe_step = n

            # Display the current step
            self.action_display_current_step()
        except:
            print('Hmmm, I\'m not sure what step that is. Could you rephrase that?')

        return

    def action_answer_how_to(self, action):
        '''
        Displays the search results from YouTube for 'how to <action>?'
        :param action: The action to search Youtube how to do.
        Note: Queries on YouTube have the form: https://www.youtube.com/results?search_query=how+to+<action>
        :return: None
        '''
        s = 'That\'s a good question! Here are some results I found for that: '
        s += 'https://www.youtube.com/results?search_query=how+'
        s += '+'.join(self.__remove_puncutation(action).split())
        print(s)
        return

    def action_answer_what_is(self, thing):
        '''
        Displays the search results from Google for 'what is <thing>?'
        :param thing: The string of the thing to search Google for what it is.
        Note: Queries on Google have the form: https://www.google.com/search?q=what+is+<thing>
        :return: None
        '''
        s = 'That\'s a good question! Here are some results I found for that: '
        s += 'https://www.google.com/search?q=what+is+'
        s += '+'.join(self.__remove_puncutation(thing).split())
        print(s)
        return

    def action_transform_recipe(self, transformation):
        '''
        Updates the recipe with the provided transformation.
        :param transformation: A string denoting the type of transformation from Project 2.
        :return: None
        '''
        # TODO: Implement this
        return

    def __print_transformation_options(self):
        '''
        Display the transformation options on the command line.
        :return: None
        '''
        print('\n***************************************************************')
        print('Recipe Transformation Options:\n')
        print('[0]: Make recipe healthy')
        print('[1]: Make recipe unhealthy')
        print('[2]: Make recipe vegetarian')
        print('[3]: Make recipe non-vegetarian')
        print('[4]: Make recipe Japanese')
        print('[5]: Make recipe Mexican')
        print('[6]: Make recipe Italian')
        print('[7]: Make recipe double portion')
        print('[8]: Make recipe half portion')
        print('[9]: End session')
        print('***************************************************************\n')
        return

    def __print_substitutions_performed(self, subs):
        '''
        Nicely prints out the substitution dictionary.
        :param subs: A dictionary mapping the name of the original ingredient to the name of the new ingredient.
        :return: None
        '''
        print('\n***************************************************************')
        print('SUBSTITUTIONS PERFORMED')
        print('***************************************************************')
        for key, value in subs.items():
            print(key + ' -> ' + value)

    def __remove_puncutation(self, s):
        '''
        Remove all punctuation from the given string.
        :param s: The original string.
        :return: The original string without any punctuation.
        '''
        return s.translate(str.maketrans('', '', string.punctuation))
