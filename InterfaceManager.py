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
        substitutions_performed = {}

        # Print out the recipe that was found
        print('\nFound the following recipe:\n')
        print(current_recipe)

        # Start the main user input loop
        terminate = False
        while not terminate:
            # Provide options to the user
            self.__print_transformation_options()

            # Parse in the option selected by the user
            selected_option = input('To perform an action, please input the number associated with the appropriate option: ')

            # Perform the action
            if selected_option == '0':
                current_recipe, substitutions_performed = current_recipe.transform_healthy()
                print("\nThe new, more healthy recipe is below: \n".upper())
                print(current_recipe.__str__())
                self.__print_substitutions_performed(substitutions_performed)
            elif selected_option == '1':
                current_recipe, substitutions_performed = current_recipe.transform_unhealthy()
                print("\nThe new, less healthy recipe is below: \n".upper())
                print(current_recipe.__str__())
                self.__print_substitutions_performed(substitutions_performed)
            elif selected_option == '2':
                current_recipe, substitutions_performed = current_recipe.transform_vegetarian()
                print("\nThe new, vegetarian version of the recipe is below: \n".upper())
                print(current_recipe.__str__())
                self.__print_substitutions_performed(substitutions_performed)
            elif selected_option == '3':
                current_recipe, substitutions_performed = current_recipe.transform_non_vegetarian()
                print("\nThe new, non-vegetarian version of the recipe is below: \n".upper())
                print(current_recipe.__str__())
                self.__print_substitutions_performed(substitutions_performed)
            elif selected_option == '4':
                current_recipe, substitutions_performed = current_recipe.transform_cuisine('japan')
                print("\nThe new, more Japanese version of the recipe is below: \n".upper())
                print(current_recipe.__str__())
                self.__print_substitutions_performed(substitutions_performed)
            elif selected_option == '5':
                current_recipe, substitutions_performed = current_recipe.transform_cuisine('mexico')
                print("\nThe new, more Mexican version of the recipe is below: \n".upper())
                print(current_recipe.__str__())
                self.__print_substitutions_performed(substitutions_performed)
            elif selected_option == '6':
                current_recipe = current_recipe.transform_size(2.0)
                print("\nThe new, double portion version of the recipe is below: \n".upper())
                print(current_recipe.__str__())
            elif selected_option == '7':
                current_recipe = current_recipe.transform_size(0.5)
                print("\nThe new, half portion version of the recipe is below: \n".upper())
                print(current_recipe.__str__())
            elif selected_option == '8':
                terminate = True
            else:
                print('Invalid input. Please input a number between 0 and 6.')

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
        print('[5]: Make recipe Mexican')
        print('[6]: Make recipe double portion')
        print('[7]: Make recipe half portion')
        print('[8]: End session')
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