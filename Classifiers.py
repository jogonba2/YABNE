#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

""" Add here your classifiers (scikit-learn convention) """

from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.preprocessing import normalize

class Classifiers:

    @staticmethod
    def mlp_nn_classifier(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = MLPClassifier(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def gaussian_nb(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = GaussianNB(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def svm(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = svm.SVC(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def ada_boost(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = AdaBoostClassifier(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def random_forest(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = RandomForestClassifier(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def decision_tree(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = DecisionTreeClassifier(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def bernoulli_nb(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = BernoulliNB(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def multinomial_nb(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = MultinomialNB(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def nearest_centroid(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = NearestCentroid(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def k_nearest_neighbors(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = KNeighborsClassifier(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def gaussian_process_classifier(X, Y, parameters):
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]
        clf = GaussianProcessClassifier(**method_params)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def example_classifier(X, Y, parameters):
        norm_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]["norm"]
        method_params = parameters["static"]["params"]["strategies"]["ml_model"]["params"]["clf"]
        X = normalize(X, **norm_params)
        clf = KNeighborsClassifier(**method_params)
        clf.fit(X, Y)
        return clf

