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
