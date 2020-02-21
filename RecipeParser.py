import urllib3 as ul
from bs4 import BeautifulSoup
import re
import requests
import Recipe

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
