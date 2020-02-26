import pandas as pd
import os
import pprint

# IMPORTANT: SUBSTITUTION DICTIONARY INFORMATION and OFFICIAL CUISINE TYPE / COUNTRY NAMES
cuisine_types = ['japan', 'mexico']
substitution_dictionary_name = 'SUB'

class ConfigManager:
    '''
    Configuration Manager

    Handles reading in and processing the necessary files all in one place, and produces the necessary data structures
    for performing actions within the recipe transformer.
    '''
    def __init__(self):
        pass

    def load_csv(self, csv_path):
        return pd.read_csv(csv_path)

    def create_substitution_dictionaries(self):
        '''
        Writes out a substitution dictionary for each type of transformation to a Python file for immediate use in the
        program.
        :return: None
        '''
        # Open the python file to write the dictionaries to
        with open('substitutions.py', 'w+') as f:
            f.write(substitution_dictionary_name + ' = {}\n\n')
            # Pass the file to the other dictionary creation methods to create all the necessary transformation dictionaries
            self.create_vegetarian_substitution_dictionaries(f)
            self.create_healthy_substitution_dictionaries(f)
            self.create_cuisine_substitution_dictionaries(f)


    def create_cuisine_substitution_dictionaries(self, output_file):
        '''
        Writes the substitution dictionaries for the cuisine transformations to the output_file provided.
        :param output_file: The .py file to write out the dictionaries to.
        :return: None
        '''

        # Initialize the cuisine type transformation dictionary
        cuisine_transforms = {}
        for cuisine in cuisine_types:
            cuisine_transforms[cuisine] = {}

            # Loop over each ingredient file in ./ingredients/
            ingredient_directory = 'ingredients'
            for filename in os.listdir(ingredient_directory):
                if filename.endswith('.csv'):
                    df = self.load_csv(ingredient_directory + '/' + filename)
                    df.fillna('', inplace=True)

                    # Split the dataframe into two components based on the country column
                    mask = df['country'] == cuisine
                    df_current_cuisine_ingredients = df[mask]
                    df_non_cuisine_ingredients = df[~mask]

                    # If the size of dataframe with all ingredients of the current cuisine is greater than 0:
                    if len(df_current_cuisine_ingredients.index) > 0:
                        # For each ingredient occ not a part of the current cuisine country:
                        for occ in df_non_cuisine_ingredients.itertuples(index=False):
                            # For each ingredient icc in the current cuisine country:
                            for icc in df_current_cuisine_ingredients.itertuples(index=False):
                                # Append icc to the list of ingredients that are a substitute for the occ
                                if occ.name not in cuisine_transforms[cuisine]:
                                    cuisine_transforms[cuisine][occ.name] = []
                                cuisine_transforms[cuisine][occ.name].append(icc.name)

        # Write out the cuisine transformation dictionary to the output python file
        for cuisine in cuisine_types:
            output_file.write(substitution_dictionary_name + '[\"' + cuisine + '\"] = ')
            output_file.write(pprint.pformat(cuisine_transforms[cuisine], compact=True, width=1000))
            output_file.write('\n\n')

        # print(cuisine_transforms)

    def create_vegetarian_substitution_dictionaries(self, output_file):
        '''

        :param output_file:
        :return:
        '''
        pass

    def create_healthy_substitution_dictionaries(self, output_file):
        '''

        :param output_file:
        :return:
        '''
        pass