# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
from rasa.core.events import Restarted

import random
import logging
import request_api

logger = logging.getLogger(__name__)
REQUESTED_SLOT = "requested_slot"

_map_int2size = {'0': 'S', '1': 'M', '2': 'L', '3': 'XL', '4': 'XXL'}

def mapping_size(weight, height, style):

    if int(weight) <= 49 and height <= '1m6':
        tmp = '0'
    elif int(weight) <= 55 and height <= '1m68':
        tmp = '1'
    elif int(weight) <= 62 and height <= '1m74':
        tmp = '2'
    elif int(weight) <= 67 and height <= '1m8':
        tmp = '3'
    else:
        tmp = '4'

    return _map_int2size[tmp]

def map_arr_to_arrDict(urls):

    tmps = []
    key = ["url"]
    for i in range(len(urls)):
        url = [urls[i]]
        zipbObj = zip(key, url)
        tmp = dict(zipbObj)
        tmps.append(tmp)

    return tmps

def get_imgs_tryon():
    imgs = []
    url = "https://mtv-fashion.com/wp-content/uploads/2017/05/ao-thun-co-tron-nam-mau-den-3.jpg"
    imgs.append(url)

    tmps = map_arr_to_arrDict(imgs)

    return tmps

def get_clothes_recommend(type_item="phông", gender="nam", color="đen"):

    imgs = request_api.get_clothes_recommend(type_item=type_item, gender=gender, color=color)
    # index = [i for i in range(0, len(imgs))]
    # irecomd = random.sample(index, k=10)
    recomds = [i for i in imgs]
    key = "buttons"
    value = {"title":"Thử mặc", "payload":"/affirm_agree"}
    tmps = map_arr_to_arrDict(recomds)
    for i in range(len(tmps)):
        tmps[i][key] = value

    return tmps

def get_suggest_stores():

    shops = ["https://shopee.vn/search?keyword=áo%20phông",
             "https://tiki.vn/search?q=áo%20phông",
             "https://www.zanado.com/thoi-trang.html?run=1&q=áo+phông",
             "https://h2tshop.com/tim?q=áo+phông",
             "https://shop.steholmes.studio/t-shirts/",
             "https://www.lazada.vn/catalog/?q=áo+phông",
             "https://canifa.com/catalogsearch/result/?q=áo+phông",
             "https://www.zalora.com.my",
             "https://shop.steholmes.studio/t-shirts/"
            ]

    prices = [request_api.random_price(),
              request_api.random_price(),
              request_api.random_price(),
              request_api.random_price(),
              request_api.random_price(),
              request_api.random_price(),
              request_api.random_price(),
              request_api.random_price(),
              request_api.random_price(),]
    index = [i for i in range(0, 5)]
    recomd = random.sample(index, k=4)
    shops = [shops[i] for i in recomd]
    sprices = [prices[i] for i in recomd]

    return shops, sprices

def form_fillsize(numbers):

    tmps = numbers.split()
    tmps = " - ".join(tmp for tmp in tmps)
    return tmps

class ItemForm(FormAction):
    """
    this form action will get the item_group slot from user and determined
    the required slots for each item_group
    after get all the slots this will retrieval from db to return the
    search detail to user
    """
    def name(self):
        # type: () -> Text
        """Unique indentifier of the form"""
        return "item_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list required slots that the form has to fill"""

        return ["type_item", "gender", "color"]

    @staticmethod
    def type_items()-> List[Text]:
        return ["phông", "thể thao", 'sơ mi', 'váy']

    def request_next_slot(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type: Dict[Text, Any]
    ):  # type: (...) -> Optional[List[Dict]]
        """Request next slots and utter tample if needed else return None"""
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                logger.debug("Request next slot '{}'".format(slot))

                if slot == 'type_item':
                    type_items = random.sample(self.type_items(), k=3)
                    dispatcher.utter_template('utter_suggest_type_item', tracker, type1=type_items[0].upper(),
                                              type2=type_items[1].upper(), type3=type_items[2])
                dispatcher.utter_template("utter_ask_{}".format(slot), tracker, silent_fail=False, **tracker.slots)
                return [SlotSet(REQUESTED_SLOT, slot)]

        return None

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do affter all required slots arre filled"""

        dispatcher.utter_template("utter_item_finding", tracker)
        return []

class ActionRecommendClothes(Action):

    def name(self):  # type: () -> Text
        return "action_recommend_clothes"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:  Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        color = tracker.get_slot('color')
        clothes = get_clothes_recommend(color=color)
        # print(clothes)
        dispatcher.utter_template("utter_recommend_item_base_img",
                                  tracker,
                                  image=clothes)
        # dispatcher.utter_template("utter_button_tryon", tracker)

        return []


class ActionSuggestItem(Action):

    def name(self):  # type: () -> Text
        return "action_suggest_item"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:  Dict[Text, Any],) -> List[Dict[Text, Any]]:
        item_1 = "Áo 1"
        item_2 = "Áo 2"
        item_3 = "Áo 3"
        dispatcher.utter_template("utter_suggest_item", tracker, item1=item_1.upper(), item2=item_2.upper(), item3=item_3.upper())

        return []

class ActionRespondTryon(Action):
    def name(self):  # type: () -> Text
        return "action_respond_tryon"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:  Dict[Text, Any], ) -> List[Dict[Text, Any]]:

        imgs = get_imgs_tryon()
        url = "https://fakerpbc247.files.wordpress.com/2019/08/87803.png"
        arrUrl = [url]
        tmps = map_arr_to_arrDict(arrUrl)
        # size = tracker.get_slot("size")

        dispatcher.utter_template("utter_respond_trying", tracker)
        dispatcher.utter_template("utter_respond_title", tracker)
        dispatcher.utter_template("utter_respond_tryon", tracker, image=tmps)

        return []

class ActionRecommendSize(Action):
    def name(self):  # type: () -> Text
        return "action_recommend_size"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:  Dict[Text, Any], ) -> List[Dict[Text, Any]]:

        numbers = tracker.get_slot('numbers')
        tmp = form_fillsize(numbers)
        url = request_api.get_response_recommend_size(tmp)
        # print(url)
        # url = "https://fakerpbc247.files.wordpress.com/2019/08/87803.png"
        # url = "http://" + url
        arrUrl = [url]
        tmps = map_arr_to_arrDict(arrUrl)
        # print(tmps)

        dispatcher.utter_template("utter_recommend_size", tracker, image=tmps)

        return []

class ActionSuggestStores(Action):
    def name(self):  # type: () -> Text
        return "action_suggest_stores"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:  Dict[Text, Any], ) -> List[Dict[Text, Any]]:

        shops, sprices = get_suggest_stores()

        dispatcher.utter_template("utter_suggest_stores_title", tracker)
        for i in range(len(shops)):
            dispatcher.utter_template("utter_suggest_stores", tracker, shop=shops[i], price=sprices[i])

class ActionSuggestRecommendSize(Action):
    def name(self):  # type: () -> Text
        return "action_suggest_recommend_size"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:  Dict[Text, Any], ) -> List[Dict[Text, Any]]:

        url = request_api.get_recommend_size()
        print(url)
        # url = "fakerpbc247.files.wordpress.com/2019/08/recommend_size1.png"
        # url = "http://" + url
        # print(url)
        arrUrl = [url]
        tmps = map_arr_to_arrDict(arrUrl)
        # print(tmps)

        dispatcher.utter_template("utter_suggest_recommend_size", tracker, image=tmps)

class ActionRestart(Action):

    def name(self):
        return 'action_restart'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template('utter_restart', tracker)
        return[Restarted()]
    
class ActionResetSlot(Action):  

    def name(self):
        return 'action_reset_slot'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet('style', None),
                SlotSet('numbers', None),
                SlotSet('type_item', None),
                SlotSet('gender', None),
                SlotSet('color', None)]