#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Receiveoffers.py

""" Add here your methods for receive offers """

from random import randint

class ReceiveOffers:

    @staticmethod
    def receive_max_offers(offers, parameters):
        res_utilities = []
        utility_func = parameters["static"]["params"]["strategies"]["utility_type"]["func"]
        acceptance_type = parameters["static"]["params"]["strategies"]["acceptance_type"]["func"]
        s = parameters["dynamic"]["s"]
        t = parameters["dynamic"]["t"]

        for offer in offers:
            res_utilities.append(utility_func(offer, parameters))
        max_utility, pos_max_utility = float("-inf"), -1
        for i in range(len(res_utilities)):
            if res_utilities[i]>=max_utility: max_utility, pos_max_utility = res_utilities[i], i

        parameters["dynamic"]["memory_received_offers"] += res_utilities
        parameters["dynamic"]["utility"] = max_utility
        accept = acceptance_type(parameters)
        if accept:
            parameters["dynamic"]["accepted_offers"].append([offers[pos_max_utility], t, 1])
            return offers[pos_max_utility]
        else:
            parameters["dynamic"]["revoked_offers"].append([offers[pos_max_utility], t, 0])
            return False


    @staticmethod
    def receive_random_offers(offers, parameters):
        acceptance_type = parameters["static"]["params"]["strategies"]["acceptance_type"]["func"]
        utility_func = parameters["static"]["params"]["strategies"]["utility_type"]["func"]
        offer = offers[randint(0, len(offers)-1)]
        parameters["dynamic"]["utility"] = utility_func(offer, parameters)
        accept = acceptance_type(parameters)
        if accept:
            return offer
        else:
            return False