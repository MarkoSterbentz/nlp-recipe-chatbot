class Ingredient:
    '''
    Ingredient

    name: the name of the ingredient
    quantity: the numerical amount of the ingredient
    measurement_unit: the unit of measurement for this ingredient (e.g. cup, teaspoon, ml, etc.)
    descriptor: any extra description of the ingredient (e.g. fresh, extra-virgin, etc.)
    preparation: any extra description of how the ingredient is prepared (e.g. finely chopped, minced, etc.)
    '''
    def __init__(self, name='', quantity=None, measurement_unit='', descriptor=[], preparation=[], text=''):
        self.name = name
        self.quantity = quantity
        self.measurement_unit = measurement_unit
        self.descriptor = descriptor
        self.preparation = preparation
        self.text = text

    def pretty_print(self):
        '''
        Prints out the ingredient as a nicely formatted string.
        :return: None
        '''
        print('    ' + self.text)

    def scale(self, scale_factor):
        '''
        Scale the quantity of the ingredient.
        :param scale_factor: The amount to scale the ingredient by
        :return: None
        '''
        self.quantity = scale_factor * self.quantity
