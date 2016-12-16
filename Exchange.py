from Utils import Utils
from Agent import Agent
from Messages import Messages
from json import load
import pickle

class Exchange:

    @staticmethod
    def deal(agent_one, agent_two, first_random=True, n_offers=1, corpus_path="./",
             use_knowledge=True, save_corpus=False, show_offers=True):

        dealer_one, dealer_two = Utils.select_first_dealer(agent_one, agent_two, first_random) ; t = 0
        offers_register = []

        dealer_one.set_oponent(dealer_two.get_name()) ; dealer_two.set_oponent(dealer_one.get_name())

        # Entrenar los modelos para cada agente #
        if use_knowledge:
            dealer_one.load_oponent_knowledge(corpus_path+"/"+dealer_two.get_name()+".dump")
            dealer_two.load_oponent_knowledge(corpus_path + "/" + dealer_one.get_name() + ".dump")

        while True:
            print("Step ",t,"...",end="\r")
            dealer_one.set_t(t)
            dealer_two.set_t(t)
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

        if save_corpus:
            with open(corpus_path+"/"+dealer_one.get_name()+".dump","ab") as fd:
                pickle.dump(dealer_one.get_knowledge(), fd)

            with open(corpus_path+"/"+dealer_two.get_name()+".dump","ab") as fd:
                pickle.dump(dealer_two.get_knowledge(), fd)

        if show_offers: print(Messages.show_offers(offers_register))


if __name__ == "__main__":
    with open("./config.json", "r") as fd:
        config_file = load(fd)
        agent_one = Agent(definition_json=config_file["agents"]["AgentOne"])
        agent_two = Agent(definition_json=config_file["agents"]["AgentTwo"])
        corpus_path = config_file["knowledge"]["corpus_path"]
        use_knowledge = config_file["knowledge"]["use_knowledge"]
        save_corpus = config_file["knowledge"]["save_corpus"]
        n_offers = config_file["params"]["n_offers"]
        show_offers = config_file["params"]["show_offers"]
        first_random = config_file["params"]["first_random"]
        version = config_file["project_info"]["version"]
        author = config_file["project_info"]["author"]
        Messages.header()
        Exchange.deal(agent_one, agent_two, first_random=first_random, n_offers=n_offers, corpus_path=corpus_path,
                      use_knowledge=use_knowledge, save_corpus=save_corpus, show_offers=show_offers)
        Messages.footer(version, author)

