#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

from time import sleep

class Messages:

    @staticmethod
    def accepted_deal_message(dealer_accept, dealer_proposal, step,
                              benefits_accept, benefits_proposal,
                              dealer_accept_s, dealer_proposal_s, offer):

        return "\n\n* Deal accepted by dealer %s at step %d * \n\n " \
               "· Benefits dealer %s: %f \n " \
               "· Benefits dealer %s: %f \n " \
               "· Concession dealer %s: %f \n " \
               "· Concession dealer %s: %f \n " \
               "· Offer: %s \n" % (dealer_accept, step, dealer_accept, benefits_accept,
                                   dealer_proposal, benefits_proposal, dealer_accept,
                                   dealer_accept_s, dealer_proposal, dealer_proposal_s, offer)

    @staticmethod
    def deal_revoked(dealer, step):
        return "\n\n* Deal revoked by dealer %s at step %d * \n\n " % (dealer, step)

    @staticmethod
    def show_offers(offers):
        res = "\n\n* Offers * \n\n"
        for i in range(len(offers)):
            res += "- Step %d from %s : \n\n" % (i, offers[i][0])
            for offer in  offers[i][1]:
                res += "\t %s \n" % (offer)
            res += "\n"
        return res

    @staticmethod
    def footer(version, author):
        res = "* Negotiation v" + str(version) + " , " + str(author) + " *\n"
        a = ""
        for i in range(len(res)):
            a += res[i]
            sleep(0.01)
            print(a, end="\r")

    @staticmethod
    def header():
        print("\n")

    @staticmethod
    def bilateral():
        return " *************\n * Bilateral * \n ************* \n\n"

    @staticmethod
    def tournament():
        return " **************\n * Tournament * \n ************** \n\n"

    @staticmethod
    def tournament_statistics(statistics):
        res = "*** Tournament statistics *** \n\n"
        for agent in statistics:
            res += agent + " : \n\n"
            for stat in statistics[agent]:
                res += "\t · " + stat[0] + " : " + str(stat[1]) + "\n"
            res += "\n"
        return res

    @staticmethod
    def tournament_round(i, agent_one_name, agent_two_name):
        return "Round %i : %s - %s\n" % (i, agent_one_name, agent_two_name)

    @staticmethod
    def less_two_agents():
        return "At least two agents.\n"

    @staticmethod
    def installing(package):
        return "Installing %s ..." % (package)

    @staticmethod
    def agent_definition_error(name, error):
        return "Error in agent %s definition, field %s is not defined" % (name, error)

    @staticmethod
    def usage():
        return "\nUsage: python Main.py config_file.json\n"