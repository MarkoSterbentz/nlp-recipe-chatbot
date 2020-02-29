# CS 337 - Recipe Transformer

This project takes link to a recipe from AllRecipes.com, scrapes it, and allows for a variety of transformations to be
applied to it according to the user's input. The transformations include making the recipe more healthy or unhealthy,
making the recipe vegetarian or non-vegetarian, doubling the portion size or cutting it in half, and transforming the
ingredients used to be more like a traditional Japanese, Mexican, or Italian dish.

Team Members (Group 4): Cameron Barrie, Alexander Reneau, Marko Sterbentz

The repository for this project can be found on GitHub: https://github.com/MarkoSterbentz/nlp-recipe-transformer

## Required Packages
- Pandas (for data containers)
  - Installation: with `pip install pandas`
  - Webpage: https://pandas.pydata.org/
- Spacy (for general NLP tasks)
  - Installation: `pip install -U spacy`
  - We use the `en_core_web_sm` model, which can be installed with `python -m spacy download en_core_web_sm` after installing Spacy.
- BeautifulSoup (for web scraping)
  - Installation: `pip install beautifulsoup4`
  - Webpage: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

Note that a full list of all packages installed can be found in requirements.txt.

## How it Works
### Parsing and Internal Representation
Parsing of recipe pages from allrecipes.com is done using the BeautifulSoup library. For a
given recipe page, the ingredients are found by extracting the content of HTML tags having
a particular attribute corresponding to an ingredient item. The raw text for each of the
resulting ingredient items is broken further into ingredient name, quantity, measurement unit,
descriptor (e.g. BROWN rice, ENGLISH cucumber, etc.), and preparation (e.g. chopped, melted,
etc.). Quantity is identified by extracting the beginning number from the ingredient item
text. The remainder of the ingredient subparts are identified by using the Spacy library to
extract the part-of-speech of each token. The first noun following the quantity is considered
to be the measurement unit if it exists in our unit gazetteer, any additional nouns are
considered to be a part of the ingredient name, verbs are considered to be ingredient
preparation steps, and adjectives are considered to be descriptors.

As with the ingredients, the cooking steps of the recipe are extracted from the page using
the content of HTML tags having attributes corresponding major cooking steps. Individidual
steps within each major step are
differentiated by considering each sencence a new step. Each of these steps are then scanned
to identify whether they contain ingredients from the recipe's ingredient
list. If so, the ingredient in the text of the cooking step is replaced by a placeholder,
which makes substitutions easier during recipe transformations.

Cooking tools and methods are found by comparing all words in the text of all ingredients and
cooking steps with items in our tools and methods gazetteers. Matches are added to the recipe's
list of tools or methods respectively.

The final internal representation of a recipe is as follows. Each recipe object has a list of
ingredients objects, cooking step objects, tool strings, and method strings. Each ingredient
object has a name, quantity, measurement unit, list of descriptors, and list of preparation
steps. Each cooking step object has a list of ingredients strings and also has the text of
the cooking step, where mentioned ingredients have been replaced by placeholders.

### Substitutions



