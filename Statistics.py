#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

""" Add here your classifiers (scikit-learn convention) """

import numpy as np

class Statistics:

    @staticmethod
    def all(utilities):
        statistics = {}
        for agent in utilities:
            statistics[agent] = [("mean", np.mean(utilities[agent])),
                                 ("min", np.amin(utilities[agent])),
                                 ("max", np.amax(utilities[agent])),
                                 ("std", np.std(utilities[agent])),
                                 ("var", np.var(utilities[agent])),
                                 ("first percentile", np.percentile(utilities[agent], 1)),
                                 ("second percentile", np.percentile(utilities[agent], 2)),
                                 ("third percentile", np.percentile(utilities[agent], 3))]
        return statistics