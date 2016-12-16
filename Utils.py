""" Add here your stuff """

from random import shuffle
from numpy import array
import json


class Utils:

    @staticmethod
    def select_first_dealer(agent_one, agent_two, first_random):
        if first_random:
            a = [agent_one, agent_two] ; shuffle(a)
            dealer_one, dealer_two = a.pop(), a.pop()
        else:
            dealer_one, dealer_two = agent_one, agent_two
        return dealer_one, dealer_two

    @staticmethod
    def load_json(json_file):
        with open(json_file) as fd:
            return json.load(fd)

    @staticmethod
    def register_corpus(offers, dealer_one_values_attr, dealer_two_values_attr):
        h = {}
        for offer_register in offers:
            if offer_register[0] not in h:
                h[offer_register[0]] = []
                for offer in offer_register:
                    continue

    @staticmethod
    def convert_knowledge_to_samples(offers):
        X, Y = [], []
        for offer in offers:
            X.append([])
            for key in offer[0]:
                X[-1].append(offer[0][key])
            for i in range(1, len(offer)-1):
                X[-1].append(offer[i])
            Y.append(offer[-1])
        return X, Y

    @staticmethod
    def convert_knowledge_to_sample_test(offer, t):
        X = []
        for key in offer:
            X.append(offer[key])
        X.append(t)
        return X