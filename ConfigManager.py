import pandas as pd

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
        pass