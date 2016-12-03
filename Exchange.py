from Utils import Utils
from Agent import Agent
from Messages import Messages

class Exchange:

    @staticmethod
    def deal(agent_one, agent_two, first_random=True, n_offers=1):

        dealer_one, dealer_two = Utils.select_first_dealer(agent_one, agent_two, first_random) ; t = 0
        offers_register = []
        while True:

            if t%2==0:
                offers = dealer_one.emit_n_offers(n_offers)
                offers_register.append((dealer_one.get_name(), offers))
                offers_accepted = dealer_two.receive_offers(offers)


            else:
                offers = dealer_two.emit_n_offers(n_offers)
                offers_register.append((dealer_two.get_name(), offers))
                offers_accepted = dealer_one.receive_offers(offers)

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

        print(Messages.show_offers(offers_register))


if __name__ == "__main__":
    tyrion = Agent(definition_json="./Bots/Tyrion.json")
    john_snow = Agent(definition_json="./Bots/JohnSnow.json")
    Exchange.deal(tyrion, john_snow)


