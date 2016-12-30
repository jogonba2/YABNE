#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

from Utils import Utils
from Messages import Messages
from Graphics import Graphics
import pickle

class Exchange:

    @staticmethod
    def deal(agent_one, agent_two, first_random=True, n_offers=1, corpus_path="./",
             save_corpus=False, show_offers=True, show_graphic_process=True, graphic_interactive=False):

        dealer_one, dealer_two = Utils.select_first_dealer(agent_one, agent_two, first_random) ; t = 0
        offers_register = []
        dealer_one.set_oponent(dealer_two.get_name()) ; dealer_two.set_oponent(dealer_one.get_name())
        proposal_offers_one_x, proposal_offers_one_y = [], []
        proposal_offers_two_x, proposal_offers_two_y = [], []

        # Entrenar los modelos para cada agente #
        if dealer_one.get_using_knowledge(): dealer_one.load_oponent_knowledge(corpus_path + "/" + dealer_two.get_name() + ".dump")
        if dealer_two.get_using_knowledge(): dealer_two.load_oponent_knowledge(corpus_path + "/" + dealer_one.get_name() + ".dump")

        while True:
            print("Step ",t,"...", end="\r")
            dealer_one.set_t(t)
            dealer_two.set_t(t)
            if t%2==0:
                offers = dealer_one.emit_n_offers(n_offers)
                offers_register.append((dealer_one.get_name(), offers))
                offers_accepted = dealer_two.receive_offers(offers)
                for offer in offers:
                    proposal_offers_one_x.append(agent_one.get_benefits(offer))
                    proposal_offers_one_y.append(agent_two.get_benefits(offer))

            else:
                offers = dealer_two.emit_n_offers(n_offers)
                offers_register.append((dealer_two.get_name(), offers))
                offers_accepted = dealer_one.receive_offers(offers)
                for offer in offers:
                    proposal_offers_two_x.append(agent_one.get_benefits(offer))
                    proposal_offers_two_y.append(agent_two.get_benefits(offer))

            if offers_accepted:
                dealer_accept = dealer_two if t%2==0 else dealer_one
                dealer_proposal = dealer_two if t%2!=0 else dealer_one
                dealer_accept_name = dealer_two.get_name() if t%2==0 else dealer_one.get_name()
                dealer_proposal_name = dealer_two.get_name() if t%2!=0 else dealer_one.get_name()
                print(Messages.accepted_deal_message(dealer_accept=dealer_accept_name,
                                                     dealer_proposal=dealer_proposal_name,
                                                     step=t,
                                                     benefits_accept=dealer_accept.get_benefits(offers_accepted),
                                                     benefits_proposal=dealer_proposal.get_benefits(offers_accepted),
                                                     dealer_accept_s = dealer_accept.get_s(),
                                                     dealer_proposal_s = dealer_proposal.get_s(),
                                                     offer=offers_accepted))
                break

            if not dealer_one.ready(t):
                print(Messages.deal_revoked(dealer=dealer_one.get_name(), step=t)) ; break

            if not dealer_two.ready(t):
                print(Messages.deal_revoked(dealer=dealer_two.get_name(), step=t)) ; break

            dealer_one.update_s(t)
            dealer_two.update_s(t)
            t += 1

        if save_corpus:
            with open(corpus_path+"/"+dealer_one.get_name()+".dump","ab") as fd:
                pickle.dump(dealer_one.get_knowledge(), fd)

            with open(corpus_path+"/"+dealer_two.get_name()+".dump","ab") as fd:
                pickle.dump(dealer_two.get_knowledge(), fd)

        if show_offers: print(Messages.show_offers(offers_register))


        if offers_accepted:
            if show_graphic_process:
                accepted_offer = 0 < len(offers_accepted)
                dealer_proposal = 2 if t % 2 != 0 else 1
                if graphic_interactive:
                    Graphics.draw_offers(proposal_offers_one_x, proposal_offers_one_y,
                                         proposal_offers_two_x, proposal_offers_two_y,
                                         accepted_offer, dealer_proposal, dealer_one.get_name(),
                                         dealer_two.get_name())
                else:
                    Graphics.draw_offers_all(proposal_offers_one_x, proposal_offers_one_y,
                                             proposal_offers_two_x, proposal_offers_two_y,
                                             accepted_offer, dealer_proposal, dealer_one.get_name(),
                                             dealer_two.get_name())

            return {dealer_one.get_name(): dealer_one.get_benefits(offers_accepted),
                    dealer_two.get_name(): dealer_two.get_benefits(offers_accepted)}