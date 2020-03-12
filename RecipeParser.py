from bs4 import BeautifulSoup
from CookingStep import CookingStep
import ConfigManager
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

def substring_insert(ingredient_list, ingredient):
    new_ingredient = ingredient.name
    if len(new_ingredient) > 0 and new_ingredient[-1] == 's':
        new_ingredient = new_ingredient[:-1]
    for i, ing in enumerate(ingredient_list):
        list_ingredient = ing.name
        if len(list_ingredient) > 0 and list_ingredient[-1] == 's':
            list_ingredient = list_ingredient[:-1]
        if new_ingredient in list_ingredient:
            ingredient_list.insert(i+1, ingredient)
            return
        elif list_ingredient in new_ingredient :
            ingredient_list.insert(i, ingredient)
            return
    ingredient_list.append(ingredient)
    return

def get_recipe(url):
    # try:
        cm = ConfigManager.ConfigManager()
        all_ingredients = cm.load_ingredient_set()
        nlp = spacy.load("en_core_web_sm")
        recipe_page = BeautifulSoup(requests.get(url).content, 'html.parser')

        tools = []
        methods = []

        name = recipe_page.find(id='recipe-main-content').contents[0]

        ingredients = []
        html_ingredients = recipe_page.find_all(attrs={'itemprop': 'recipeIngredient', 'data-nameid': re.compile('^[^0]')})
        for lst in html_ingredients:
            text = str(lst.contents[0])
            groups = re.search('([\d.-/ ]*)(.*)', text)
            quantity = string_to_decimal(groups.group(1).rstrip())
            ingredient_name = []
            descriptor = []
            preparation = []
            unit_specifier = re.search('^ *(\(.*\) \w+) *(.*)', groups.group(2))
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

            if ' '.join(ingredient_name) not in all_ingredients:
                temp_ingredient_name = [i for i in ingredient_name]
                temp_descriptor = [d for d in descriptor]
                while len(temp_descriptor) > 0:
                    temp_ingredient_name.insert(0, temp_descriptor[-1])
                    temp_descriptor = temp_descriptor[:-1]
                    if ' '.join(temp_ingredient_name).lower() in all_ingredients:
                        ingredient_name = temp_ingredient_name
                        descriptor = temp_descriptor
                        break

            substring_insert(ingredients, Ingredient(' '.join(ingredient_name).lower(), quantity, unit, descriptor, preparation, text))

            # Check cooking tools
            for tool in tool_list:
                if tool in text and method not in tools:
                    tools.append(tool)

            # Check cooking methods
            for method in method_list:
                if method in text and method not in methods:
                    methods.append(method)

        steps = []
        html_steps = recipe_page.find_all(class_='recipe-directions__list--item')
        for big_step in html_steps:
            if big_step.contents:
                for step in big_step.contents[0].split('. '):
                    step_ingredients = []
                    ing_num = 0
                    for ing in ingredients:
                        ing_terms = ing.name.split()
                        num_terms = len(ing_terms)
                        while num_terms > 0:
                            for idx in range(len(ing_terms) - num_terms + 1):
                                composite_term = ' '.join(ing_terms[idx:idx+num_terms])
                                search_term1 = re.compile(composite_term, re.IGNORECASE)
                                search_term2 = re.compile(composite_term[:-1], re.IGNORECASE)
                                replacement = '{' + str(ing_num) + '}'
                                if re.search(search_term1, step):
                                    step_ingredients.append(ing.name)
                                    # step = step.replace(composite_term, '{' + str(ing_num) + '}')
                                    step = re.sub(search_term1, replacement, step)
                                    ing_num += 1
                                    num_terms = 0
                                    break
                                elif composite_term[-1] == 's' and re.search(search_term2, step):
                                    step_ingredients.append(ing.name)
                                    # step = step.replace(composite_term[:-1], '{' + str(ing_num) + '}')
                                    step = re.sub(search_term2, replacement, step)
                                    ing_num += 1
                                    num_terms = 0
                                    break
                            num_terms -= 1

                    # check for quantities in step
                    quantities = []
                    for quantity_unit_match in re.finditer('(\d[\d.-/ ]*) ([^.,;: ]+)', step):
                        if quantity_unit_match.group(2) in measurement_units or re.match(' *{\d+} *', quantity_unit_match.group(2)):
                            quantities.append(string_to_decimal(quantity_unit_match.group(1)))
                            step = step.replace(quantity_unit_match.group(0), '{' + str(ing_num) + '} ' + quantity_unit_match.group(2))
                            ing_num += 1

                    steps.append(CookingStep(ingredients=step_ingredients, quantities=quantities, text=step))
                steps[-1].text = steps[-1].text.strip().rstrip('.')

                # Check cooking tools
                for tool in tool_list:
                    if tool in big_step.contents[0] and tool not in tools:
                        tools.append(tool)

                # Check cooking methods
                for method in method_list:
                    if method in big_step.contents[0] and method not in methods:
                        methods.append(method)

        return Recipe(name, ingredients, steps, tools, methods)
    # except:
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


# print(get_recipe('https://www.allrecipes.com/recipe/20088/awesome-eggplant-rollatine/'))
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

