#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

""" Add here your concession methods """

from random import uniform
from math import e

class Concession:

    @staticmethod
    def temporal_concession(parameters):
        s = parameters["dynamic"]["s"]
        ur = parameters["static"]["params"]["general"]["ur"]
        t = parameters["dynamic"]["t"]
        revoke_step = parameters["static"]["params"]["general"]["revoke_step"]
        beta = parameters["static"]["params"]["strategies"]["concession_type"]["params"]["beta"]
        return s - ((s - ur) * ((t / revoke_step) ** (s / beta)))

    @staticmethod
    def behavioural_relative_concession(parameters):
        s = parameters["dynamic"]["s"]
        ur = parameters["static"]["params"]["general"]["ur"]
        memory_received_offers = parameters["dynamic"]["memory_received_offers"]
        memory_proposal_offers = parameters["dynamic"]["memory_proposal_offers"]
        delta = parameters["static"]["params"]["strategies"]["concession_type"]["params"]["delta"]
        if 0<len(memory_received_offers)-delta<len(memory_received_offers):
            return min(s, max(ur, ((s - memory_received_offers[-delta+1]) /
                                     (s - memory_received_offers[-delta])) *
                                      memory_proposal_offers[-1]))
        else:
            return Concession.temporal_concession(parameters)

    @staticmethod
    def behavioural_absolute_concession(parameters):
        s = parameters["dynamic"]["s"]
        ur = parameters["static"]["params"]["general"]["ur"]
        memory_received_offers = parameters["dynamic"]["memory_received_offers"]
        memory_proposal_offers = parameters["dynamic"]["memory_proposal_offers"]
        delta = parameters["static"]["params"]["strategies"]["concession_type"]["params"]["delta"]
        if 0<len(memory_received_offers)-delta<len(memory_received_offers) and 0<len(memory_proposal_offers):
            return min(s, max(ur, memory_proposal_offers[-1] - memory_received_offers[-delta+1] - memory_received_offers[-delta]))
        else:
            return Concession.temporal_concession(parameters)

    @staticmethod
    def behavioural_averaged_concession(parameters):
        s = parameters["dynamic"]["s"]
        ur = parameters["static"]["params"]["general"]["ur"]
        memory_received_offers = parameters["dynamic"]["memory_received_offers"]
        memory_proposal_offers = parameters["dynamic"]["memory_proposal_offers"]
        delta = parameters["static"]["params"]["strategies"]["concession_type"]["params"]["delta"]
        if 0<len(memory_received_offers)-delta<len(memory_received_offers) and 0<len(memory_proposal_offers):
            return min(s, max(ur, ((s - memory_received_offers[-1]) /
                                     (s - memory_received_offers[-delta+1])) *
                                      memory_proposal_offers[-1]))
        else:
            return Concession.temporal_concession(parameters)

    @staticmethod
    def non_concession(parameters): return 1

    @staticmethod
    def random_concession(parameters): return uniform(0, 1)

    #http: // mathworld.wolfram.com / ExponentialDecay.html
    @staticmethod
    def exponential_decay(parameters):
        s = parameters["dynamic"]["s"]
        t = parameters["dynamic"]["t"]
        l = None
        if "lambda" in parameters["dynamic"]:
            l = parameters["dynamic"]["lambda"]
        else:
            l = parameters["static"]["params"] \
                          ["strategies"]["concession_type"]\
                          ["params"]["lambda"]
        l = l * uniform(0, 1)
        parameters["dynamic"]["lambda"] = l
        return s*(e**(-l*t))
