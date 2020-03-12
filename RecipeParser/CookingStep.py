class CookingStep:
    '''
    Cooking Step

    ingredients: the ingredient being operated on in this cooking step
    tools: the tools used in this cooking step
    time_quantity: the amount of time needed to performing this cooking step
    time_unit: the unit of time
    '''
    def __init__(self, ingredients=[],  quantities=[], unit='', text=''):
        self.ingredients = ingredients
        self.quantities = quantities
        self.unit = unit
        self.text = text

    def __str__(self):
        '''
        :return: The cooking step as a nicely formatted string.
        '''
        ings_and_quants = self.ingredients + [str(quant).rstrip('0').rstrip('.') for quant in self.quantities]
        return self.text.format(*ings_and_quants)

