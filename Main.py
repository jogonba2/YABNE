#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

from json import load
from Agent import Agent
from Messages import Messages
from Exchange import Exchange
from Statistics import Statistics
from sys import argv

def main():
    if len(argv)!=2: print(Messages.usage()) ; exit()
    else: config_fd = argv[1]
    with open(config_fd, "r") as fd:
        config_file = load(fd)
        version = config_file["project_info"]["version"]
        author = config_file["project_info"]["author"]
        agents = []
        for agent_name in config_file["agents"]:
            agent = Agent(definition_json=config_file["agents"][agent_name])
            err = agent.get_valid()
            if err != True:
                print(Messages.agent_definition_error(agent_name, err))
                exit()
            agents.append(agent)
        corpus_path = config_file["knowledge"]["corpus_path"]
        save_corpus = config_file["knowledge"]["save_corpus"]
        n_offers = config_file["params"]["n_offers"]
        show_offers = config_file["params"]["show_offers"]
        first_random = config_file["params"]["first_random"]
        graphic_process = config_file["params"]["graphic_process"]
        graphic_interactive = config_file["params"]["graphic_interactive"]
        Messages.header()

        if len(agents)==2:
            print(Messages.bilateral())
            Exchange.deal(agents[0], agents[1], first_random=first_random, n_offers=n_offers, corpus_path=corpus_path,
                          save_corpus=save_corpus, show_offers=show_offers, show_graphic_process=graphic_process,
                          graphic_interactive=graphic_interactive)

        elif 2<len(agents):
            print(Messages.tournament())
            utilities = {}
            for agent in agents: utilities[agent.get_name()] = []
            c = 0
            for i in range(len(agents)):
                for j in range(min(len(agents)-1,i+1), len(agents)):
                    if i!=j:
                        print(Messages.tournament_round(c, agents[i].get_name(), agents[j].get_name()))
                        results = Exchange.deal(agents[i], agents[j], first_random=first_random, n_offers=n_offers,
                                                corpus_path=corpus_path, save_corpus=save_corpus, show_offers=show_offers,
                                                show_graphic_process=graphic_process, graphic_interactive=graphic_interactive)
                        utilities[agents[i].get_name()].append(results[agents[i].get_name()])
                        utilities[agents[j].get_name()].append(results[agents[j].get_name()])
                        c += 1

            print(Messages.tournament_statistics(Statistics.all(utilities)))
        else: print(Messages.less_two_agents())

if __name__ == "__main__": main()