import RecipeParser as rp


class InterfaceManager:
    '''
    Interface Manager
    Manages user interaction with the recipe transformer.
    '''

    def __init__(self, current_recipe=None, current_recipe_step=None, waiting_for_answer=False, terminate=False):
        self.current_recipe = current_recipe
        self.current_recipe_step = current_recipe_step
        self.waiting_for_answer = waiting_for_answer
        self.terminate = terminate

    def start_interaction_loop(self):
        '''
        The main loop that handles all user interaction with the user.
        :return: None
        '''

        # Print an initial welcome message
        print('Hi! I\'m Remy! Are you ready to cook?')
        self.waiting_for_answer = True

        while not self.terminate:
            # Parse the input
            user_input = input()

            # Determine the intent of the input and the action to be taken
            action_string, arg = self.determine_intent(user_input)

            # Perform the action
            if action_string == 'display_ingredient_list':
                self.action_display_ingredient_list()
            elif action_string == 'go_to_step':
                n = 0 # TODO: Determine what step the user is asking for based on the arg and the current_step_index
                self.action_go_to_step(n)
            elif action_string == 'answer_how_to':
                self.action_answer_how_to(arg)
            elif action_string == 'answer_what_is':
                self.action_answer_what_is(arg)
            elif action_string == 'terminate':
                self.terminate = True
            else:
                # Don't know what they're saying.
                print('Sorry, I didn\'t catch that. Could you try rephrasing that?')

        print('Thanks for talking with me today!')

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
        return None, None

    def action_get_url(self):
        '''
        Asks the user for a recipe URL from AllRecipes.com.
        :return: Returns the recipe object, if it was a valid URL
        '''
        original_recipe = None
        while original_recipe is None:
            url = input('Alrighty, give me a recipe from AllRecipes.com: ')

            # Initialize a Recipe object based on this recipe
            original_recipe = rp.get_recipe(url)

            if original_recipe is None:
                print('Sorry, I wasn\'t able to find a recipe there.\n')

    def action_display_ingredient_list(self):
        '''
        Displays the ingredient list of the current recipe.
        :return: None
        '''
        return

    def action_go_to_step(self, n):
        '''
        Displays the nth step of the current recipe, if it exists.
        :param n: The index of the step to display.
        :return: None
        '''
        self.current_recipe_step = n
        return

    def action_answer_how_to(self, action):
        '''
        Displays the search results from YouTube for 'how to <action>?'
        :param action: The action to search Youtube how to do.
        Note: Queries on YouTube have the form: https://www.youtube.com/results?search_query=how+to+<action>
        :return: None
        '''
        return

    def action_answer_what_is(self, thing):
        '''
        Displays the search results from Google for 'what is <thing>?'
        :param thing: The thing to search Google for what it is.
        Note: Queries on Google have the form: https://www.google.com/search?q=what+is+<thing>
        :return: None
        '''
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