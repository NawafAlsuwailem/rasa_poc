# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from actions.weather_api import city_weather


class SanedRegistrationForm(FormAction):
    def name(self):
        return "saned_cencellation_form"

    @staticmethod
    def required_slots(tracker):
        return ["nationality", "salary"]

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any],
               ) -> List[Dict]:
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nationality": [
                self.from_text(intent="inform"),
            ],
            "salary": [
                self.from_text(intent="inform"),
            ]
        }


#
class ActionWeatherAsk(Action):
    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.latest_message['text']
        print(city)
        temp = int(city_weather(city)['temp'] - 273)
        dispatcher.utter_template("utter_temp", tracker, temp=temp, city=city)

        return []


class ActionClothesAsk(Action):
    def name(self) -> Text:
        return "action_clothes_ask"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("im heeerreeeee")
        city = tracker.get_slot('city')
        print(city)

        temp = int(city_weather(city)['temp'] - 273)
        clothes = "خفيف"
        if temp < 15:
            clothes = "ثقيل"
        dispatcher.utter_template("utter_clothes_ask", tracker, temp=temp, city=city, clothes=clothes)
        return []


class ValidateSurveyForm(Action):
    def name(self) -> Text:
        return "survey_form"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: Dict,
    ) -> List[EventType]:
        required_slots = ["rating", "service"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                return [SlotSet("requested_slot", slot_name)]
        return [SlotSet("requested_slots", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_survey_thanks",
                                 Rating=tracker.get_slot("rating"),
                                 Service=tracker.get_slot("service"))