import urllib3 as ul
from bs4 import BeautifulSoup
import re
import requests
import Recipe
import json

def get_recipe(url):
    try:
        http = ul.PoolManager()
        # recipe_page = BeautifulSoup(http.request('GET', url), 'html.parser')
        recipe_page = BeautifulSoup(requests.get(url).content, 'html.parser')

        ingredients = []
        html_ingredients = recipe_page.find_all(attrs={'itemprop': 'recipeIngredient', 'data-nameid': re.compile('^[^0]')})
        for lst in html_ingredients:
            ingredients.append(lst.contents[0])

        steps = []
        html_steps = recipe_page.find_all(class_='recipe-directions__list--item')
        for big_step in html_steps:
            if big_step.contents:
                for step in big_step.contents[0].split('. '):
                    steps.append(step)
                steps[-1] = steps[-1].strip().rstrip('.')

        return Recipe.Recipe(ingredients, steps)
    except:
        return None

# get_recipe('https://www.allrecipes.com/recipe/223529/vermicelli-noodle-bowl/?internalSource=previously%20viewed&referringContentType=Homepage')
# get_recipe('https://www.allrecipes.com/recipe/57354/beef-pho/?internalSource=previously%20viewed&referringContentType=Homepage')

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
