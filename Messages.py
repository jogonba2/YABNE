
class Messages:

    @staticmethod
    def accepted_deal_message(dealer_accept, dealer_proposal, step,
                              benefits_accept, benefits_proposal,
                              dealer_accept_s, dealer_proposal_s, offer):

        return "* Deal accepted by dealer %s at step %d * \n\n " \
               "· Benefits dealer %s: %f \n " \
               "· Benefits dealer %s: %f \n " \
               "· Concession dealer %s: %f \n " \
               "· Concession dealer %s: %f \n " \
               "· Offer: %s \n" % (dealer_accept, step, dealer_accept, benefits_accept,
                                   dealer_proposal, benefits_proposal, dealer_accept,
                                   dealer_accept_s, dealer_proposal, dealer_proposal_s, offer)

    @staticmethod
    def deal_revoked(dealer, step):
        return "* Deal revoked by dealer %s at step %d * \n\n " % (dealer, step)

    @staticmethod
    def show_offers(offers):
        res = "* Offers * \n\n"
        for i in range(len(offers)):
            res += "- Step %d from %s : \n\n" % (i, offers[i][0])
            for offer in  offers[i][1]:
                res += "\t %s \n" % (offer)
            res += "\n"
        return res