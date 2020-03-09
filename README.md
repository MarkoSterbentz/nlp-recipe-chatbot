# CS 337 - Recipe Chatbot

This project aims to provide a conversational interface for interacting with the recipe transformer. 

Team Members (Group 4): Cameron Barrie, Alexander Reneau, Marko Sterbentz

The repository for this project can be found on GitHub: https://github.com/MarkoSterbentz/nlp-recipe-chatbot


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

## Running the Project
This project requires Python 3.6+. It can be ran on the command line and terminal using the following input:

`python main.py`


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
the content of HTML tags having attributes corresponding major cooking steps. Individual
steps within each major step are
differentiated by considering each sentence a new step. Each of these steps are then scanned
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

### Substitutions and Transformations
In order to perform the substitutions, it was first necessary to construct a set of ingredient types and properties
associated with each of these types. The properties for each ingredient type can be found within the
 `ingredient_type_properties.csv` file in the `config` directory. A list of ingredients that are a part of each of these
 types can be found in the `ingredients` directory.

When developing the of hierarchy of ingredient types, we considered how it would relate to each of the recipe transformations
that could be applied. In addition, ingredient properties like texture and cooking method were considered to ensure that the
substitution of one ingredient for another would maintain the consistency of the recipe. For each of the ingredient types,
there is a mapping to another ingredient type for each transformation. With these mappings in hand,
the substitution dictionary found in `substitutions.py` can be generated. This allows for a fast runtime look-up to
be done when deciding whether an ingredient should be substituted out for a specific transformation, and what the new
ingredient to replace it should be.

There are 9 transformations that the user can apply to any given recipe:
1. To vegetarian (make the recipe vegetarian)
2. To non-vegetarian (make the recipe non-vegetarian)
3. To healthy (make the recipe healthier)
4. To unhealthy (make the recipe less healthy)
5. To Japanese (make the recipe incorporate conventional Japanese ingredients)
6. To Mexican (make the recipe incorporate conventional Mexican ingredients)
7. To Italian (make the recipe incorporate conventional Italian ingredients)
8. Increase portion quantities
9. Decrease portion quantities

The general algorithm for performing a transformation is roughly the same across each type (except for increasing/decreasing
portion quantities), with some transformation specific additions. For each of the ingredients in the recipe, we
check and see if there is a valid substitution for this ingredient within the pre-generated substitution dictionary.
If there is, we get the list of candidate substitutions. For each of these, we substitute it in unless
it is already a part of the recipe. This involves updating the ingredient list of the recipe, as well as
ensuring that the cooking step(s) associated with this ingredient are properly updated for the new ingredient.

When making a recipe more or less healthy, there is an additional step that either increases or decreases the quantity of
unhealthy ingredients in the recipe. For the non-vegetarian transformation, if there are no possible substitutions to
make to the recipe that would cause it to be non-vegetarian, a meat is added to the recipe and the cooking steps required
to incorporate this meat are added to the recipe.
