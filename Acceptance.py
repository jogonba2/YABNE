#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

""" Add here your acceptance methods """

from random import uniform
from math import sqrt

class Acceptance:

    @staticmethod
    def rational(parameters):
        return parameters["dynamic"]["utility"] >= parameters["dynamic"]["s"]

    @staticmethod
    def random(parameters):
        return parameters["dynamic"]["utility"] >= uniform(0, 1)

    @staticmethod
    def greater_than_sqrt(parameters):
        return parameters["dynamic"]["utility"] >= parameters["dynamic"]["s"] + sqrt(parameters["dynamic"]["s"])

    @staticmethod
    def rational_until_end(parameters):
        if parameters["dynamic"]["t"]==parameters["static"]["params"]["general"]["revoke_step"]-1:
            return True
        else:
            return parameters["dynamic"]["utility"] >= parameters["dynamic"]["s"]

    @staticmethod
    def accept_last_offer(parameters):
        if parameters["dynamic"]["t"]==parameters["static"]["params"]["general"]["revoke_step"]-1:
            return True
        else:
            return False