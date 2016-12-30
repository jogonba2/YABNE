#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

""" Add here your concession methods """

from random import uniform

class Concession:

    @staticmethod
    def temporal_concession(t, ur, beta, revoke_step, s):
        return s - ((s - ur) * ((t / revoke_step) ** (s / beta)))

    @staticmethod
    def behavioural_relative_concession(t, ur, memory_proposal_offers, memory_received_offers, delta, s):
        return min(s, max(ur, ((s - memory_received_offers[-delta+1]) /
                                 (s - memory_received_offers[-delta])) *
                                  memory_proposal_offers[-1]))

    @staticmethod
    def behavioural_absolute_concession(t, ur, memory_proposal_offers, memory_received_offers, delta, s):
        return min(s, max(ur, memory_proposal_offers[-1] - memory_received_offers[-delta+1] - memory_received_offers[-delta]))

    @staticmethod
    def behavioural_averaged_concession(t, ur, memory_proposal_offers, memory_received_offers, delta, s):
        return min(s, max(ur, ((s - memory_received_offers[-1]) /
                                 (s - memory_received_offers[-delta+1])) *
                                  memory_proposal_offers[-1]))

    @staticmethod
    def non_concession(): return 1

    @staticmethod
    def random_concession(): return uniform(0, 1)