#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

from Utils import Utils
from Utility import Utility
from Concession import Concession
from Acceptance import Acceptance
from Offers import Offers
from Classifiers import Classifiers
from Messages import Messages

from pickle import load

class Agent:

    def __init__(self, definition_json):
        definition_json = Utils.load_json(definition_json)
        self.valid = self.__is_valid(definition_json)
        if self.valid==True:
            self.agent_name = self.__load_field(definition_json["agent_info"], "name")
            self.agent_gender = self.__load_field(definition_json["agent_info"], "gender")
            self.agent_country = self.__load_field(definition_json["agent_info"], "country")
            self.agent_birthday = self.__load_field(definition_json["agent_info"], "birthday")
            self.agent_reputation = self.__load_field(definition_json["agent_info"], "reputation")
            self.description = self.__load_field(definition_json["agent_info"], "description")
            self.attributes = self.__load_field(definition_json, "attributes")
            self.revoke_step = self.__load_field(definition_json, "revoke_step")
            self.weights_attr = self.__load_field(definition_json, "weights_attr")
            self.values_attr = self.__load_field(definition_json, "values_attr")
            self.ur = self.__load_field(definition_json, "ur")
            self.delta = self.__load_field(definition_json, "delta")
            self.beta  = self.__load_field(definition_json, "beta")
            self.s = self.__load_field(definition_json, "s")
            self.window_offer = self.__load_field(definition_json, "window_offer")
            self.concession_type = getattr(Concession, self.__load_field(definition_json, "concession_type"))
            self.utility_type = getattr(Utility, self.__load_field(definition_json, "utility_type"))
            self.acceptance_type = getattr(Acceptance, self.__load_field(definition_json, "acceptance_type"))
            self.offer_type = getattr(Offers, self.__load_field(definition_json, "offer_type"))
            try: self.ml_type = getattr(Classifiers, self.__load_field(definition_json, "ml_model"))
            except: pass
            self.oponent_model = None
            self.memory_proposal_offers = []
            self.memory_received_offers = []
            self.t = 0
            self.accepted_offers = []
            self.revoked_offers = []
            self.oponent_agent = None
            self.using_oponent_knowledge = self.__load_field(definition_json["agent_info"], "using_oponent_knowledge")
            self.upper_bound_knowledge = self.__load_field(definition_json, "upper_bound_knowledge")

    def __is_valid(self, definition_json):
        if not "agent_info" in definition_json: return "agent_info"
        if not "attributes" in definition_json: return "attributes"
        if not "revoke_step" in definition_json: return "revoke_step"
        if not "weights_attr" in definition_json: return "weights_attr"
        if not "values_attr" in definition_json: return "values_attr"
        if not "ur" in definition_json: return "ur"
        if not "s" in definition_json: return "s"
        if not "concession_type" in definition_json: return "concession_type"
        if not "utility_type" in definition_json: return "utility_type"
        if not "acceptance_type" in definition_json: return "acceptance_type"
        if not "offer_type" in definition_json: return "offer_type"
        if not "using_oponent_knowledge" in definition_json["agent_info"]: return "using_oponent_knowledge"
        return True

    def __load_field(self, field, attribute):
        if attribute in field: return field[attribute]
        return None

    def emit_offer(self):
        space = {}
        for attr in self.attributes:
            if self.attributes[attr]=="integer" or self.attributes[attr]=="float":
                space[attr] = (self.attributes[attr],
                              self.values_attr[self.attributes[attr]][attr]["properties"]["min"],
                              self.values_attr[self.attributes[attr]][attr]["properties"]["max"])
            elif self.attributes[attr]=="categorical":
                space[attr] = (self.attributes[attr],
                               self.values_attr[self.attributes[attr]][attr]["properties"]["choices"])
        #print(self.agent_name+","+str(self.s)+","+str(self.window_offer)+","+str(self.s+self.window_offer))
        max_range = min(1, (self.s + self.window_offer)) if self.window_offer != None else 1
        offer, utility = self.offer_type(space, self.s, max_range, self.utility_type, self.attributes, self.weights_attr,
                                         self.values_attr, self.using_oponent_knowledge,self.oponent_model, self.t,
                                         self.upper_bound_knowledge)
        self.memory_proposal_offers.append(utility)
        self.accepted_offers.append([offer, self.t, 1])
        return offer

    def emit_n_offers(self, n):
        return [self.emit_offer() for i in range(n)]

    def receive_offers(self, offers):
        res_utilities = []
        for offer in offers:
            res_utilities.append(self.utility_type(self.attributes, self.weights_attr, self.values_attr, offer))
        max_utility, pos_max_utility = float("-inf"), -1
        for i in range(len(res_utilities)):
            if res_utilities[i]>=max_utility: max_utility, pos_max_utility = res_utilities[i], i
        self.memory_received_offers += res_utilities
        accept = self.acceptance_type(max_utility, self.s)
        if accept:
            self.accepted_offers.append([offers[pos_max_utility], self.t, 1])
            return offers[pos_max_utility]
        else:
            self.revoked_offers.append([offers[pos_max_utility], self.t, 0])
            return False

    # Solo cuando se lleven \delta+1 iteración se cambiará. Se parte inicialmente de concesión temporal #
    def update_s(self, t):
        if self.concession_type==Concession.temporal_concession:
            self.s = self.concession_type(t, self.ur, self.beta, self.revoke_step, self.s)

        elif self.concession_type == Concession.behavioural_relative_concession or \
             self.concession_type == Concession.behavioural_absolute_concession or \
             self.concession_type == Concession.behavioural_averaged_concession:

            if t<=self.delta*2:
                self.s = Concession.temporal_concession(t, self.ur, self.beta, self.revoke_step, self.s)
            else:
                self.s = self.concession_type(t, self.ur, self.memory_proposal_offers, self.memory_received_offers, self.delta, self.s)

        elif self.concession_type==Concession.non_concession() or \
             self.concession_type==Concession.random_concession():

            self.s = self.concession_type()

    def get_benefits(self, offer):
        return self.utility_type(self.attributes, self.weights_attr, self.values_attr, offer)

    def get_valid(self): return self.valid

    def ready(self, t):
        return t<self.revoke_step

    def get_name(self):
        return self.agent_name

    def get_using_knowledge(self):
        return self.using_oponent_knowledge

    def get_weights_attr(self):
        return self.weights_attr

    def get_values_attr(self):
        return self.values_attr

    def get_ur(self):
        return self.ur

    def get_s(self):
        return self.s

    def get_window_offer(self):
        return self.window_offer

    def get_knowledge(self):
        return self.accepted_offers+self.revoked_offers

    def set_t(self, t): self.t = t

    def get_memory_proposal_offers(self):
        return self.memory_proposal_offers

    def get_memory_received_offers(self):
        return self.memory_received_offers

    def set_oponent(self, oponent_agent): self.oponent_agent = oponent_agent

    def load_oponent_knowledge(self, dump_file):
        with open(dump_file, "rb") as fd:
            oponent_knowledge = load(fd)
            #print("Para el agente: ",self.agent_name+" conocimiento sobre: ",self.oponent_agent+": "+str(oponent_knowledge[0:5]))
            X, Y = Utils.convert_knowledge_to_samples(oponent_knowledge)
            self.oponent_model = self.ml_type(X, Y)


if __name__ == "__main__":
    tyrion = Agent(definition_json="./Bots/Tyrion.json")
    """
    print(tyrion.receive_offer({"price": 5000,
                               "color": "green",
                               "abs" : "no"
                               }))
    """
   # print(tyrion.update_s(5))
    print(tyrion.get_benefits({'abs': 'yes', 'price': 1675, 'color': 'red'}))