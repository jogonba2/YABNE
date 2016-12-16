""" Add here your concession methods """

from random import uniform

class Concession:

    @staticmethod
    def temporal_concession(t, ur, beta, revoke_step):
        return 1.0 - ((1.0 - ur) * ((t / revoke_step) ** (1.0 / beta)))

    @staticmethod
    def behavioural_relative_concession(t, ur, memory_proposal_offers, memory_received_offers, delta):
        return min(1.0, max(ur, ((1.0 - memory_received_offers[-delta+1]) /
                                 (1.0 - memory_received_offers[-delta])) *
                                  memory_proposal_offers[-1]))

    @staticmethod
    def behavioural_absolute_concession(t, ur, memory_proposal_offers, memory_received_offers, delta):
        return min(1.0, max(ur, memory_proposal_offers[-1] - memory_received_offers[-delta+1] - memory_received_offers[-delta]))

    @staticmethod
    def behavioural_averaged_concession(t, ur, memory_proposal_offers, memory_received_offers, delta):
        return min(1.0, max(ur, ((1.0 - memory_received_offers[-1]) /
                                 (1.0 - memory_received_offers[-delta+1])) *
                                  memory_proposal_offers[-1]))

    @staticmethod
    def non_concession(): return 1

    @staticmethod
    def random_concession(): return uniform(0, 1)