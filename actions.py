# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from RecipeParser.InterfaceManager import InterfaceManager
from RecipeParser import RecipeParser

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# TODO: Do this dynamically using user input.
interface = InterfaceManager(current_recipe=RecipeParser.get_recipe('https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/'), current_recipe_step=0)

class ActionDisplayIngredients(Action):

    def name(self) -> Text:
        return "action_display_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=interface.action_display_ingredient_list())

        return []

class ActionDisplayIngredients(Action):

    def name(self) -> Text:
        return "action_display_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=interface.action_display_current_step())

        return []
