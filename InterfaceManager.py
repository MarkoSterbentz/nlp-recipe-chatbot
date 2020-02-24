import RecipeParser as rp


class InterfaceManager:
    '''
    Interface Manager
    Manages user interaction with the recipe transformer.
    '''

    def __init__(self):
        pass

    def start_interaction_loop(self):
        '''
        The main loop that handles all user interaction with the user.
        :return: None
        '''

        print('Welcome to the Recipe Transformer!')

        # Get the user input for the recipe url
        original_recipe = None
        while original_recipe is None:
            url = input('Please enter a URL from AllRecipes.com: ')

            # Initialize a Recipe object based on this recipe
            original_recipe = rp.get_recipe(url)

            if original_recipe is None:
                print('Unable to find a recipe at the provided URL.\n')

        # Store the current recipe to be transformed by the next user input
        current_recipe = original_recipe

        # Print out the recipe that was found
        current_recipe.pretty_print()

        # Start the main user input loop
        terminate = False
        while not terminate:
            # Provide options to the user
            self.__print_transformation_options()

            # Parse in the option selected by the user
            selected_option = input('To perform an action, please input the number associated with the appropriate option: ')

            # Perform the action
            if selected_option == '0':
                current_recipe = current_recipe.transform_healthy()
            elif selected_option == '1':
                current_recipe = current_recipe.transform_unhealthy()
            elif selected_option == '2':
                current_recipe = current_recipe.transform_vegetarian()
            elif selected_option == '3':
                current_recipe = current_recipe.transform_non_vegetarian()
            elif selected_option == '4':
                current_recipe = current_recipe.transform_Japanese()
            elif selected_option == '5':
                terminate = True
            else:
                print('Invalid input. Please input a number between 0 and 5.')

        print('Thank you for using our recipe transformer!')

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
        print('[5]: End session')
        print('***************************************************************\n')
        return