class CookingStep:
    '''
    Cooking Step

    ingredients: the ingredient being operated on in this cooking step
    tools: the tools used in this cooking step
    time_quantity: the amount of time needed to performing this cooking step
    time_unit: the unit of time
    '''
    def __init__(self, ingredients, tools, method, time_quantity, time_unit):
        self.ingredients = ingredients
        self.tools = tools
        self.method = method
        self.time_quantity = time_quantity
        self.time_unit = time_unit
        pass

    def change_cooking_method(self):
        pass

    def pretty_print(self):
        pass