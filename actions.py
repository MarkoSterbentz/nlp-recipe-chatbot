# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from RecipeParser.InterfaceManager import InterfaceManager
from RecipeParser import RecipeParser

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

interface = InterfaceManager()


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

        website_url = str(tracker.get_slot('website'))
        success = interface.action_get_recipe(website_url)

        return []


class ActionGoToStep(Action):

    def name(self) -> Text:
        return "action_go_to_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        step_number = str(tracker.get_slot('step_number'))

        if step_number == 'first':
            success, step_text = interface.action_go_to_first_step()
        elif step_number == 'next':
            success, step_text = interface.action_go_to_step(interface.current_recipe_step + 1)
        elif step_number == 'previous':
            success, step_text = interface.action_go_to_step(interface.current_recipe_step - 1)
        elif step_number == 'last':
            success, step_text = interface.action_go_to_last_step()
        else:
            try:
                num = int(step_number) - 1
                success, step_text = interface.action_go_to_step(num)
            except:
                success = False
                step_text = None

        if success:
            dispatcher.utter_message(text=step_text)

        return []


class ActionAnswerHowTo(Action):

    def name(self) -> Text:
        return "action_answer_how_to"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        how_to_object = str(tracker.get_slot('how_to_object'))

        # dispatcher.utter_message(text="found the following for the how_to_object: " + str(how_to_object))

        dispatcher.utter_message(text=interface.action_answer_how_to(how_to_object))

        return []


class ActionAnswerWhatIs(Action):

    def name(self) -> Text:
        return "action_answer_what_is"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        what_is_object = str(tracker.get_slot('what_is_object'))

        # dispatcher.utter_message(text= "found the following for the what_is_object: " + str(what_is_object))

        dispatcher.utter_message(text=interface.action_answer_what_is(what_is_object))

        return []

class ActionTransformRecipe(Action):

    def name(self) -> Text:
        return "action_transform_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrive the Rasa slot with the proper information
        transformation_type = str(tracker.get_slot('transformation_type'))

        dispatcher.utter_message(text="found the following for the transformation_type: " + str(transformation_type))

        healthy_alts = ['healthy', 'nutritious', 'healthier', 'better']
        unhealthy_alts = ['unhealthy', 'non-nutritious', 'bad']
        vegetarian_alts = ['vegetarian', 'veggie']
        nonvegetarian_alts = ['nonvegetarian', 'non-vegetarian', 'carnivore', 'carnivorous']
        mexican_alts = ['mexican', 'mexico']
        italian_alts = ['italy', 'italian']
        japanese_alts = ['japan', 'japanese']
        double_alts = ['double', 'more', 'big', 'bigger']
        half_alts = ['half', 'less', 'small', 'smaller']

        if transformation_type is not None:
            if transformation_type in healthy_alts:
                results = interface.action_transform_recipe('healthy')
                if results is not None:
                    dispatcher.utter_message(text=results)
            elif transformation_type in unhealthy_alts:
                results = interface.action_transform_recipe('unhealthy')
                if results is not None:
                    dispatcher.utter_message(text=results)
            elif transformation_type in vegetarian_alts:
                results = interface.action_transform_recipe('vegetarian')
                if results is not None:
                    dispatcher.utter_message(text=results)
            elif transformation_type in nonvegetarian_alts:
                results = interface.action_transform_recipe('non-vegetarian')
                if results is not None:
                    dispatcher.utter_message(text=results)
            elif transformation_type in italian_alts:
                results = interface.action_transform_recipe('italian')
                if results is not None:
                    dispatcher.utter_message(text=results)
            elif transformation_type in mexican_alts:
                results = interface.action_transform_recipe('mexican')
                if results is not None:
                    dispatcher.utter_message(text=results)
            elif transformation_type in japanese_alts:
                results = interface.action_transform_recipe('japanese')
                if results is not None:
                    dispatcher.utter_message(text=results)
            elif transformation_type in double_alts:
                results = interface.action_transform_recipe('double')
                if results is not None:
                    dispatcher.utter_message(text=results)
            elif transformation_type in half_alts:
                results = interface.action_transform_recipe('half')
                if results is not None:
                    dispatcher.utter_message(text=results)

        return []

