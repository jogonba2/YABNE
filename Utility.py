#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

""" Add here your utility methods """

class Utility:

    @staticmethod
    def linear(offer, parameters):
        attributes = parameters["static"]["domain"]["attributes"]
        values_attr = parameters["static"]["domain"]["values_attr"]
        weights_attr = parameters["static"]["domain"]["weights_attr"]

        utility = 0
        for item in offer:
            value_item = offer[item]
            type_item = attributes[item]
            for condition in values_attr[type_item][item]["conditions"]:
                if type_item=="integer" or type_item=="float":
                    left_bound = values_attr[type_item][item]["conditions"][condition][0]
                    right_bound = values_attr[type_item][item]["conditions"][condition][1]
                    if left_bound<=value_item<=right_bound:
                        value_item = values_attr[type_item][item]["conditions"][condition][2]
                        break

                elif type_item=="categorical":
                    if value_item==values_attr[type_item][item]["conditions"][condition][0]:
                        value_item = values_attr[type_item][item]["conditions"][condition][1]
                        break

                else: return 0
            utility += weights_attr[item] * value_item
        if 1<utility:
            print("BAD")
            print(offer)
            print(values_attr)
        return utility

