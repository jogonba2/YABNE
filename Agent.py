#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

from Utils import Utils
from Utility import Utility
from Concession import Concession
from Acceptance import Acceptance
from GenerateOffers import GenerateOffers
from ReceiveOffers import ReceiveOffers
from Classifiers import Classifiers
from Messages import Messages

from pickle import load

class Agent:

    def __init__(self, definition_json):
        self.definition_json = Utils.load_json(definition_json)
        if self.__is_valid()==True:
            self.rol = self.__load_field(self.definition_json, "rol") ; self.__load_rol_attrs()
            self.params_definition = self.definition_json["params"]
            self.__load_parameters()
            self.__get_attr_strategies()

    def __is_valid(self):
        if "agent_info" not in self.definition_json: return "agent_info"
        if "rol" not in self.definition_json: return "rol"
        if "params" not in self.definition_json: return "params"
        return True

    def __load_parameters(self):
        self.parameters = {
                            "static": {
                               "info" : self.definition_json["agent_info"],
                               "params": self.params_definition,
                               "domain": {
                                   "weights_attr": self.weights_attr,
                                   "values_attr": self.values_attr,
                                   "attributes": self.attributes
                               }
                           },

                           "dynamic": { "oponent_model" : None,
                                        "memory_proposal_offers" : [],
                                        "memory_received_offers" : [],
                                        "t" : 0,
                                        "s" : self.params_definition["general"]["s"],
                                        "accepted_offers" : [],
                                        "revoked_offers" : [],
                                        "oponent_agent" : None
                              }
                           }

    def __get_attr_strategies(self):
        for strategy in self.parameters["static"]["params"]["strategies"]:
            module_name = self.parameters["static"]["params"]["strategies"][strategy]["module"]
            module = getattr(__import__(module_name), module_name)
            name   = self.parameters["static"]["params"]["strategies"][strategy]["func"]
            self.parameters["static"]["params"]["strategies"][strategy]["func"] = getattr(module, name)

    def __load_rol_attrs(self):
        rol_json = Utils.load_json(self.rol)
        self.weights_attr = self.__load_field(rol_json, "weights_attr")
        self.values_attr = self.__load_field(rol_json, "values_attr")
        self.attributes = self.__load_field(rol_json, "attributes")

    def __load_field(self, field, attribute):
        if attribute in field: return field[attribute]
        return None

    def emit_offer(self):

        def __generate_space():
            space = {}
            for attr in self.attributes:
                if self.attributes[attr]=="integer" or self.attributes[attr]=="float":
                    space[attr] = (self.attributes[attr],
                                  self.values_attr[self.attributes[attr]][attr]["properties"]["min"],
                                  self.values_attr[self.attributes[attr]][attr]["properties"]["max"])
                elif self.attributes[attr]=="categorical":
                    space[attr] = (self.attributes[attr],
                                   self.values_attr[self.attributes[attr]][attr]["properties"]["choices"])
            return space

        space        = __generate_space()
        s            = self.parameters["dynamic"]["s"]
        window_offer = self.parameters["static"]["params"]["general"]["window_offer"]
        offer_func   = self.parameters["static"]["params"]["strategies"]["generate_offer_type"]["func"]
        self.parameters["dynamic"]["max_range"] = min(1, (s + window_offer)) if window_offer != None else 1
        offer, utility = offer_func(space, self.parameters)
        self.parameters["dynamic"]["memory_proposal_offers"].append(utility)
        self.parameters["dynamic"]["accepted_offers"].append([offer, self.parameters["dynamic"]["t"], 1])
        return offer

    def emit_n_offers(self, n):
        return [self.emit_offer() for i in range(n)]

    def receive_offers(self, offers):
        receive_offer_func = self.parameters["static"]["params"]["strategies"]["receive_offer_type"]["func"]
        return receive_offer_func(offers, self.parameters)

    # Solo cuando se lleven \delta+1 iteración se cambiará. Se parte inicialmente de concesión temporal #
    def update_s(self, t):
        self.parameters["dynamic"]["t"] = t
        concession_func = self.parameters["static"]["params"]["strategies"]["concession_type"]["func"]
        self.parameters["dynamic"]["s"] = concession_func(self.parameters)

    def get_benefits(self, offer):
        utility_func = self.parameters["static"]["params"]["strategies"]["utility_type"]["func"]
        return utility_func(offer, self.parameters)

    def ready(self, t):
        return t<self.parameters["static"]["params"]["general"]["revoke_step"]

    def get_name(self):
        return self.definition_json["agent_info"]["name"]

    def get_using_knowledge(self):
        return self.parameters["static"]["params"]["general"]["use_knowledge"]

    def get_weights_attr(self):
        return self.parameters["static"]["domain"]["weights_attr"]

    def get_valid(self):
        return self.__is_valid()

    def get_values_attr(self):
        return self.parameters["static"]["domain"]["values_weights_attr"]

    def get_ur(self):
        return self.parameters["static"]["params"]["general"]["ur"]

    def get_s(self):
        return self.parameters["dynamic"]["s"]

    def get_window_offer(self):
        return self.parameters["static"]["params"]["general"]["window_offer"]

    def get_knowledge(self):
        return self.parameters["dynamic"]["accepted_offers"] + self.parameters["dynamic"]["revoked_offers"]

    def set_t(self, t): self.parameters["dynamic"]["t"]

    def get_memory_proposal_offers(self):
        return self.parameters["dynamic"]["memory_proposal_offers"]

    def get_memory_received_offers(self):
        return self.parameters["dynamic"]["memory_received_offers"]

    def set_oponent(self, oponent_agent):
        self.parameters["dynamic"]["oponent_agent"] = oponent_agent

    def load_oponent_knowledge(self, dump_file):
        with open(dump_file, "rb") as fd:
            oponent_knowledge = load(fd)
            #print("Para el agente: ",self.agent_name+" conocimiento sobre: ",self.oponent_agent+": "+str(oponent_knowledge[0:5]))
            ml_type = self.parameters["static"]["params"]["strategies"]["ml_model"]["func"]
            X, Y = Utils.convert_knowledge_to_samples(oponent_knowledge)
            self.parameters["dynamic"]["oponent_model"] = ml_type(X, Y, self.parameters)