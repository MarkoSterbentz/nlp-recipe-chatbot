# CS 337 - Recipe Chatbot

This project aims to provide a conversational interface for interacting with the recipe transformer. 

Team Members (Group 4): Cameron Barrie, Alexander Reneau, Marko Sterbentz

The repository for this project can be found on GitHub: https://github.com/MarkoSterbentz/nlp-recipe-chatbot


## Required Packages
- Rasa
  - Installation `pip install rasa`
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

## Installation

*Note: The following installation instructions were tested on MacOS 10.14, and assumes that Anaconda is installed. This 
is primarily needed if you are having difficulties installing Rasa or any of the packages within an existing environment.*

It is recommended that you start by setting up a new virtual environment. We do this through Anaconda with the following command:

`conda create -n <env_name>`

Then, activate this environment so that we can start installing packages there:

`source activate <env_name>`

Install pip in this environment:

`conda install pip`

Switch to a Python version in this environment that is compatible with Tensorflow, and thus Rasa as well:

`conda install python=3.7.5`

Install rasa:

`pip install rasa`

Alternatively, you can also run `pip install -r requirements` in the base project directory to install everything that
is required for this project.


## Running the Project
This project requires Python 3.6+. It can be ran on the command line and terminal using the following input:

`python main.py`


## How it Works
To be determined...
