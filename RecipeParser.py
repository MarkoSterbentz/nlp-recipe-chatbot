from bs4 import BeautifulSoup
from fractions import Fraction
from Ingredient import Ingredient
import re
from Recipe import Recipe
import requests
import spacy

with open('measurement_units.csv', 'r') as f:
    measurement_units = [line.strip() for line in f.readlines()]

def string_to_decimal(string_number):
    try:
        num = float(sum(Fraction(s) for s in string_number.split()))
    except:
        num = None
    return num


def get_recipe(url):
  # try:
        nlp = spacy.load("en_core_web_sm")
        recipe_page = BeautifulSoup(requests.get(url).content, 'html.parser')

        ingredients = []
        html_ingredients = recipe_page.find_all(attrs={'itemprop': 'recipeIngredient', 'data-nameid': re.compile('^[^0]')})
        for lst in html_ingredients:
            text = str(lst.contents[0])
            groups = re.search('([\d.-/ ]*)(.*)', text)
            quantity = string_to_decimal(groups.group(1).rstrip())
            ingredient_name = []
            descriptor = []
            preparation = []
            unit = ''

            tokens = nlp(groups.group(2))
            for token in tokens:
                if token.i == 0 and token.lemma_ in measurement_units:
                    unit = token.lemma_
                elif token.pos_ in ['NUM', 'NOUN', 'PRON', 'PROPN']:
                    ingredient_name.append(token.string.strip())
                elif token.pos_ == 'VERB':
                    preparation.append(token.string.strip())
                elif token.pos_ in 'ADJ':
                    descriptor.append(token.string.strip())

            ingredients.append(Ingredient(' '.join(ingredient_name), quantity, unit, descriptor, preparation, text))

        steps = []
        html_steps = recipe_page.find_all(class_='recipe-directions__list--item')
        for big_step in html_steps:
            if big_step.contents:
                for step in big_step.contents[0].split('. '):
                    steps.append(step)
                steps[-1] = steps[-1].strip().rstrip('.')

        return Recipe(ingredients, steps)
  # except:
  #     return None


# print(get_recipe('https://www.allrecipes.com/recipe/269592/pork-chops-in-garlic-mushroom-sauce/?internalSource=previously%20viewed&referringContentType=Homepage').pretty_print())
# print('')
print(get_recipe('https://www.allrecipes.com/recipe/223529/vermicelli-noodle-bowl/?internalSource=previously%20viewed&referringContentType=Homepage').pretty_print())
print('')
print(get_recipe('https://www.allrecipes.com/recipe/57354/beef-pho/?internalSource=previously%20viewed&referringContentType=Homepage').pretty_print())
print('')
print(get_recipe('https://www.allrecipes.com/recipe/270310/instant-pot-italian-wedding-soup/?internalSource=previously%20viewed&referringContentType=Homepage').pretty_print())
