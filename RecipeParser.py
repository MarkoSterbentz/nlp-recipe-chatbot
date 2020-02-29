from bs4 import BeautifulSoup
from CookingStep import CookingStep
from fractions import Fraction
from Ingredient import Ingredient
import json
import re
from Recipe import Recipe
import requests
import spacy

with open('configs/measurement_units.csv', 'r') as f:
    measurement_units = [line.strip() for line in f.readlines()]
with open('configs/tools.txt', 'r') as f:
    tool_list = [line.strip() for line in f.readlines()]
with open('configs/methods.txt', 'r') as f:
    method_list = [line.strip() for line in f.readlines()]

def string_to_decimal(string_number):
    try:
        num = float(sum(Fraction(s) for s in string_number.split()))
    except:
        num = None
    return num


def get_recipe(url):
    try:
        nlp = spacy.load("en_core_web_sm")
        recipe_page = BeautifulSoup(requests.get(url).content, 'html.parser')

        tools = []
        methods = []

        ingredients = []
        html_ingredients = recipe_page.find_all(attrs={'itemprop': 'recipeIngredient', 'data-nameid': re.compile('^[^0]')})
        for lst in html_ingredients:
            text = str(lst.contents[0])
            groups = re.search('([\d.-/ ]*)(.*)', text)
            quantity = string_to_decimal(groups.group(1).rstrip())
            ingredient_name = []
            descriptor = []
            preparation = []
            unit_specifier = re.search('(\(.*\) \w+) *(.*)', groups.group(2))
            unit = ''
            if unit_specifier is not None:
                unit += unit_specifier.group(1)
                tokens = nlp(unit_specifier.group(2))
            else:
                tokens = nlp(groups.group(2))

            for token in tokens:
                if token.i == 0 and token.lemma_ in measurement_units:
                    unit += ' ' + token.lemma_
                    unit = unit.lstrip()
                elif token.pos_ in ['NUM', 'NOUN', 'PRON', 'PROPN']:
                    ingredient_name.append(token.string.strip())
                elif token.pos_ == 'VERB':
                    preparation.append(token.string.strip())
                elif token.pos_ in 'ADJ':
                    descriptor.append(token.string.strip())

            # Check cooking tools
            for tool in tool_list:
                if tool in text and method not in tools:
                    tools.append(tool)

            # Check cooking methods
            for method in method_list:
                if method in text and method not in methods:
                    methods.append(method)

            ingredients.append(Ingredient(' '.join(ingredient_name), quantity, unit, descriptor, preparation, text))

        steps = []
        html_steps = recipe_page.find_all(class_='recipe-directions__list--item')
        for big_step in html_steps:
            if big_step.contents:
                for step in big_step.contents[0].split('. '):
                    step_ingredients = []
                    ing_num = 0
                    for ing in ingredients:
                        if ing.name in step:
                            step_ingredients.append(ing.name)
                            step = step.replace(ing.name, '{' + str(ing_num) + '}')
                            ing_num += 1
                        else:
                            for ing_part in ing.name.split():
                                if ing_part in step:
                                    step_ingredients.append(ing.name)
                                    step = step.replace(ing_part, '{' + str(ing_num) + '}')
                                    ing_num += 1
                                    break
                    steps.append(CookingStep(ingredients=step_ingredients, text=step))
                steps[-1].text = steps[-1].text.strip().rstrip('.')

                # Check cooking tools
                for tool in tool_list:
                    if tool in big_step.contents[0] and tool not in tools:
                        tools.append(tool)

                # Check cooking methods
                for method in method_list:
                    if method in big_step.contents[0] and method not in methods:
                        methods.append(method)

        return Recipe(ingredients, steps, tools, methods)
    except:
        print('Unable to build recipe object from url.')
        return None

def get_cuisine_recipe_urls(base_url, output_file, limit=100):
    '''
    Writes out a JSON file containing all recipes found for the given World Cuisine URL from AllRecipes.com.
    :param base_url: A URL from AllRecipes.com's world-cuisine section.
    :param output_file: The output file where the results will be written to.
    :param limit: The maximum number of recipes to find.
    :return: The list of recipe URLs.
    '''

    # Iterate through pages of recipes until there are enough
    page_number = 0
    recipe_dict = {}
    while len(recipe_dict) < limit:
        search_url = base_url.replace('%s', str(page_number))

        page_html = requests.get(search_url)

        page_graph = BeautifulSoup(page_html.content, features="lxml")

        found_recipes = [recipe.a['href'] for recipe in \
                         page_graph.find_all('div', {'class': 'grid-card-image-container'})]

        if len(found_recipes) == 0:
            break

        for r in found_recipes:
            recipe_dict[r] = None

        page_number += 1

    # Write out the JSON file of these recipes URL
    recipe_urls = list(recipe_dict.keys())[0:limit]
    with open(output_file, 'w+') as outfile:
        json.dump(recipe_urls, outfile)

    return recipe_urls


def get_japanese_recipe_urls(limit=100):
    '''
    Writes out a JSON file containing URLs of popular Japanese recipes.
    :param limit: The maximum number of recipes to retrieve.
    :return: The list of recipe urls.
    '''

    # The URL for finding Japanese cuisine recipes
    base_url = 'https://www.allrecipes.com/recipes/699/world-cuisine/asian/japanese/?page=%s'
    output_file = 'world_cuisine_recipe_urls/japanese_recipe_urls.json'

    return get_cuisine_recipe_urls(base_url, output_file)


def get_mexican_recipes(limit=100):
    '''
    Writes out a JSON file containing URLs of popular Mexican recipes.
    :param limit: The maximum number of recipes to retrieve.
    :return: The list of recipe urls.
    '''

    # The URL for finding Mexican cuisine recipes
    base_url = 'https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/?page=%s'
    output_file = 'world_cuisine_recipe_urls/mexican_recipe_urls.json'

    return get_cuisine_recipe_urls(base_url, output_file)


# print(get_recipe('https://www.allrecipes.com/recipe/269592/pork-chops-in-garlic-mushroom-sauce/?internalSource=previously%20viewed&referringContentType=Homepage'))
# print('')
# noodle_recipe = get_recipe('https://www.allrecipes.com/recipe/223529/vermicelli-noodle-bowl/?internalSource=previously%20viewed&referringContentType=Homepage')
# print(noodle_recipe)
# old_ingredients = ['white vinegar', 'lettuce', 'carrots']
# old_ingredient_objects = []
# for ing in noodle_recipe.ingredients:
#     if ing.name in old_ingredients:
#         old_ingredient_objects.append(copy.deepcopy(ing))
# new_ingredients = ['red wine vinegar', 'spinach', 'beets']
# for i in range(len(old_ingredient_objects)):
#     noodle_recipe.substitute_ingredients(old_ingredient_objects[i], new_ingredients[i])
# print(noodle_recipe)
# print('')
# print(get_recipe('https://www.allrecipes.com/recipe/57354/beef-pho/?internalSource=previously%20viewed&referringContentType=Homepage'))
# print('')
# print(get_recipe('https://www.allrecipes.com/recipe/270310/instant-pot-italian-wedding-soup/?internalSource=previously%20viewed&referringContentType=Homepage'))
# print('')
# print(get_recipe('https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/'))

