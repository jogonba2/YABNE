from random import shuffle
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