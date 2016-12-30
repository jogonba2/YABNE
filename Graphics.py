#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

import matplotlib.pyplot as plt

class Graphics:

    @staticmethod
    def draw_offers(proposal_offers_one_x, proposal_offers_one_y,
                    proposal_offers_two_x, proposal_offers_two_y,
                    accepted_offer, last_proposal, agent_one_name,
                    agent_two_name):


        minlen = min(len(proposal_offers_one_x), len(proposal_offers_two_x))
        plt.xlabel(agent_one_name)
        plt.ylabel(agent_two_name)
        plt.ion()
        for i in range(minlen):
            plt.plot(proposal_offers_one_x[0:i], proposal_offers_one_y[0:i] , linestyle='-', marker='^', color='b', linewidth=0.3, markersize=8)
            plt.plot(proposal_offers_two_x[0:i], proposal_offers_two_y[0:i], linestyle='-', marker='^', color='g', linewidth=0.3, markersize=8)
            plt.pause(0.005)
        if accepted_offer:
            if last_proposal == 1:
                plt.plot(proposal_offers_one_x, proposal_offers_one_y, linestyle='-', marker='^', color='b', linewidth=0.3, markersize=8)
                plt.plot(proposal_offers_one_x[-1], proposal_offers_one_y[-1], linestyle='-', marker='s', color='r', markersize=8)
            else:
                plt.plot(proposal_offers_two_x, proposal_offers_two_y, linestyle='-', marker='^', color='g', linewidth=0.3, markersize=8)
                plt.plot(proposal_offers_two_x[-1], proposal_offers_two_y[-1], linestyle='-', marker='s', color='r', markersize=8)
        plt.show(block=True)

    @staticmethod
    def draw_offers_all(proposal_offers_one_x, proposal_offers_one_y,
                    proposal_offers_two_x, proposal_offers_two_y,
                    accepted_offer, last_proposal, agent_one_name,
                    agent_two_name):
        plt.xlabel(agent_one_name)
        plt.ylabel(agent_two_name)
        plt.plot(proposal_offers_one_x, proposal_offers_one_y, linestyle='-', marker='^', color='b', linewidth=0.3, markersize=8)
        plt.plot(proposal_offers_two_x, proposal_offers_two_y, linestyle='-', marker='^', color='g', linewidth=0.3, markersize=8)
        if accepted_offer:
            if last_proposal==1:
                plt.plot(proposal_offers_one_x[-1], proposal_offers_one_y[-1], linestyle='-', marker='s', color='r', markersize=8)
            else:
                plt.plot(proposal_offers_two_x[-1], proposal_offers_two_y[-1], linestyle='-', marker='s', color='r', markersize=8)

        plt.show()
