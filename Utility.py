""" Add here your utility methods """

class Utility:

    @staticmethod
    def linear(attributes, weights_attrs, values_attrs, offer):
        utility = 0
        for item in offer:
            value_item = offer[item]
            type_item = attributes[item]

            for condition in values_attrs[type_item][item]["conditions"]:
                if type_item=="integer" or type_item=="float":
                    left_bound = values_attrs[type_item][item]["conditions"][condition][0]
                    right_bound = values_attrs[type_item][item]["conditions"][condition][1]
                    if left_bound<=value_item<right_bound:
                        value_item = values_attrs[type_item][item]["conditions"][condition][2]
                        break

                elif type_item=="categorical":
                    if value_item==values_attrs[type_item][item]["conditions"][condition][0]:
                        value_item = values_attrs[type_item][item]["conditions"][condition][1]
                        break

                else: return 0
            utility += weights_attrs[item] * value_item

        return utility

