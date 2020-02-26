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

    def __str__(self):
        '''
        Prints out the ingredient as a nicely formatted string.
        :return: None
        '''
        ret_val = ''
        if self.quantity > 0:
            ret_val += str(self.quantity) + ' '
        if not self.measurement_unit == '':
            ret_val += self.measurement_unit
            if self.quantity != 1.0:
                ret_val += 's'
            ret_val += ' '
        if len(self.descriptor) > 0:
            ret_val += ' '.join(self.descriptor) + ' '
        ret_val += self.name
        if len(self.preparation) > 0:
            ret_val+= ', ' + ', '.join(self.preparation)
        return ret_val

