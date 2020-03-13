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

class ActionDisplayAllSteps(Action):

    def name(self) -> Text:
        return "action_display_all_steps"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=interface.action_display_all_steps())

        return []

class ActionDisplayCurrentStep(Action):

    def name(self) -> Text:
        return "action_display_current_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=interface.action_display_current_step())

        return []

class ActionGetRecipe(Action):

    def name(self) -> Text:
        return "action_get_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        success = interface.action_get_recipe(tracker.latest_message.text)

        return []

class ActionGoToStep(Action):

    def name(self) -> Text:
        return "action_go_to_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        step_number = tracker.get_slot('step_number')
        if step_number == 'first':
            success, step_text = interface.action_go_to_first_step()
        elif step_number == 'last':
            success, step_text = interface.action_go_to_last_step()
        else:
            success, step_text = interface.action_go_to_step(step_number)

        if success:
            dispatcher.utter_message(text=step_text)

        return []

class ActionAnswerHowTo(Action):

    def name(self) -> Text:
        return "action_answer_how_to"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=interface.action_answer_how_to())

        return []

class ActionAnswerWhatIs(Action):

    def name(self) -> Text:
        return "action_answer_what_is"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=interface.action_answer_what_is())

        return []