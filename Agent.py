from Utils import Utils
from Utility import Utility
from Concession import Concession
from Acceptance import Acceptance
from Offers import Offers

class Agent:

    def __init__(self, definition_json):
        definition_json = Utils.load_json(definition_json)
        self.agent_name = definition_json["agent_name"]
        self.agent_gender = definition_json["agent_gender"]
        self.agent_country = definition_json["agent_country"]
        self.attributes = definition_json["attributes"]
        self.revoke_step = definition_json["revoke_step"]
        self.weights_attr = definition_json["weights_attr"]
        self.values_attr = definition_json["values_attr"]
        self.ur = definition_json["ur"]
        self.delta = definition_json["delta"]
        self.beta  = definition_json["beta"]
        self.s = definition_json["s"]
        self.concession_type = getattr(Concession, definition_json["concession_type"])
        self.utility_type = getattr(Utility, definition_json["utility_type"])
        self.acceptance_type = getattr(Acceptance, definition_json["acceptance_type"])
        self.offer_type = getattr(Offers, definition_json["offer_type"])
        self.memory_proposal_offers = []
        self.memory_received_offers = []

    def emit_offer(self):
        space = {}
        for attr in self.attributes:
            if self.attributes[attr]=="integer" or self.attributes[attr]=="float":
                space[attr] = (self.attributes[attr],
                              self.values_attr[self.attributes[attr]][attr]["properties"]["min"],
                              self.values_attr[self.attributes[attr]][attr]["properties"]["max"])
            elif self.attributes[attr]=="categorical":
                space[attr] = (self.attributes[attr],
                               self.values_attr[self.attributes[attr]][attr]["properties"]["choices"])
        offer, utility = self.offer_type(space, self.s, self.utility_type, self.attributes, self.weights_attr, self.values_attr)
        self.memory_proposal_offers.append(utility)
        return offer

    def emit_n_offers(self, n):
        return [self.emit_offer() for i in range(n)]

    def receive_offers(self, offers):
        res_utilities = []
        for offer in offers:
            res_utilities.append(self.utility_type(self.attributes, self.weights_attr, self.values_attr, offer))
        max_utility, pos_max_utility = float("-inf"), -1
        for i in range(len(res_utilities)):
            if res_utilities[i]>=max_utility: max_utility, pos_max_utility = res_utilities[i], i
        self.memory_received_offers += res_utilities
        accept = self.acceptance_type(max_utility, self.s)
        if accept: return offers[pos_max_utility]
        else: return False

    # Solo cuando se lleven \delta+1 iteración se cambiará. Se parte inicialmente de concesión temporal #
    def update_s(self, t):
        if self.concession_type==Concession.temporal_concession:
            self.s = self.concession_type(t, self.ur, self.beta, self.revoke_step)

        elif self.concession_type == Concession.behavioural_relative_concession or \
             self.concession_type == Concession.behavioural_absolute_concession or \
             self.concession_type == Concession.behavioural_averaged_concession:

            if t<=self.delta*2:
                self.s = Concession.temporal_concession(t, self.ur, self.beta, self.revoke_step)
            else:
                self.s = self.concession_type(t, self.ur, self.memory_proposal_offers, self.memory_received_offers, self.delta)

        elif self.concession_type==Concession.non_concession() or \
             self.concession_type==Concession.random_concession():

            self.s = self.concession_type()

    def get_benefits(self, offer):
        return self.utility_type(self.attributes, self.weights_attr, self.values_attr, offer)

    def train_oponent_model(self):
        pass

    def predict_oponent_model(self):
        pass

    def ready(self, t):
        return t<self.revoke_step

    def get_name(self):
        return self.agent_name

    def get_weights_attr(self):
        return self.weights_attr

    def get_values_attr(self):
        return self.values_attr

    def get_ur(self):
        return self.ur

    def get_s(self):
        return self.s

    def get_memory_proposal_offers(self):
        return self.memory_proposal_offers

    def get_memory_received_offers(self):
        return self.memory_received_offers

if __name__ == "__main__":
    tyrion = Agent(definition_json="./Bots/Tyrion.json")
    """
    print(tyrion.receive_offer({"price": 5000,
                               "color": "green",
                               "abs" : "no"
                               }))
    """
   # print(tyrion.update_s(5))
    print(tyrion.get_benefits({'abs': 'yes', 'price': 1675, 'color': 'red'}))