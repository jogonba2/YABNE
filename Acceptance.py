#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

""" Add here your acceptance methods """

from random import uniform

class Acceptance:

    @staticmethod
    def rational(utility, s):
        return utility >= s

    @staticmethod
    def random(utility, s):
        return utility >= uniform(0, 1)
