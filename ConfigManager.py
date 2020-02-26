import pandas as pd
import os
import pprint

# IMPORTANT: SUBSTITUTION DICTIONARY INFORMATION and OFFICIAL CUISINE TYPE / COUNTRY NAMES
cuisine_types = ['japan', 'mexico']
substitution_dictionary_name = 'SUB'
ingredient_type_props_filepath = 'configs/ingredient_type_properties.csv'
standard_transform_col_names = ['to_vegetarian','to_non_vegetarian','to_healthy','to_unhealthy']

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
            self.create_standard_substitution_dictionaries(f, standard_transform_col_names)
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

        return


    def create_standard_substitution_dictionaries(self, output_file, transform_col_names):
        '''
        Writes the substitution dictionaries for the vegetarian-based and healthy-based transformations
        to the output_file provided.
        :param output_file: The .py file to write out the dictionaries to.
        :param transform_col_name: A list of column label in the csv for the transformation type.
        :return: None
        '''

        # Load in all ingredients for ease
        ingredient_dict = self.load_ingredient_dictionary()

        for transform_name in transform_col_names:
            # Initialize the substitution dictionaries
            sub_dict = {}

            # Load the ingredient type properties into a dataframe
            df_type_properties = self.load_csv(ingredient_type_props_filepath)
            df_type_properties.fillna('', inplace=True)

            # loop through the rows (i.e. for each ingredient type)
            for row in df_type_properties.itertuples(index=False):
                current_type = getattr(row, 'name')

                # If there is a substitution type there:
                substitution_type = getattr(row, transform_name)
                if substitution_type != '':
                    # Loop over each ingredient in ingredient dictionary for that type
                    for ing in ingredient_dict[current_type]:
                        # Add the list of ingredients of the substitution type to the substitution dictionary
                        sub_dict[ing] = ingredient_dict[substitution_type]

            # Write out the substitution dictionaries to the output python file
            output_file.write(substitution_dictionary_name + '[\"' + transform_name + '\"] = ')
            output_file.write(pprint.pformat(sub_dict, compact=True, width=1000))
            output_file.write('\n\n')

        return


    def load_ingredient_dictionary(self):
        '''
        Loads all of the ingredient lists into a dictionary index by the .csv file name.
        :param ingredient_dir: The directory containing all of the .csv files of ingredients.
        :return: The dictionary mapping ingredient types to a list of those ingredients.
        '''

        ingredient_dict = {}

        ingredient_directory = 'ingredients'
        for filename in os.listdir(ingredient_directory):
            if filename.endswith('.csv'):
                df = self.load_csv(ingredient_directory + '/' + filename)
                df.fillna('', inplace=True)

                ingredient_type = os.path.basename(filename)
                ingredient_type = os.path.splitext(ingredient_type)[0]

                # Add a new dictionary entry for the current ingredient type
                ingredient_dict[ingredient_type] = []

                for row in df.itertuples(index=False):
                    ingredient_dict[ingredient_type].append(row.name)

        return ingredient_dict
