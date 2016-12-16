""" Add here your methods for generate offers """

from random import randint, uniform, choice
from deap import base, creator, tools, algorithms
from Utils import Utils

class Offers:

    # space = {(attr_1, space_1), (attr_2, space_2), ...,(attr_n, space_n) : space_i \in {(int, min, max), (float, min, max), (str, list)}} #
    @staticmethod
    def random_offer(space, s, utility_function, attributes, weights_attr, values_attr, use_knowledge, ml_model, t, upper_bound_knowledge):
        act_s = 0
        # Regular cuantas ofertas generar usando conocimiento, si se supera upper_bound se deja de tener en cuenta que el adversario acepte o no la oferta #
        iters = 0
        while act_s<s:
            res = {}
            for key in space:
                if space[key][0]=="integer": res[key] = randint(int(space[key][1]), int(space[key][2]+1))
                elif space[key][0]=="float": res[key] = uniform(space[key][1], space[key][2]+1)
                elif space[key][0]=="categorical": res[key] = choice(space[key][1])
            act_s = utility_function(attributes, weights_attr, values_attr, res)
            if use_knowledge and iters<upper_bound_knowledge:
                x = Utils.convert_knowledge_to_sample_test(res, t)
                oponent_accepts = ml_model.predict([x])[0]
                if oponent_accepts==0:
                    act_s = float("-inf")
            iters += 1
        return res, act_s

    # Only with int attributes #
    @staticmethod
    def genetic_offer(space, s, utility_function, attributes, weights_attr, values_attr, use_knowledge,
                      ml_model, t, upper_bound_knowledge, pob_size=50, prob_mutate=0.3, prob_mating=0.4, iterations=30, tournsize=2):

        iters = 0
        def transform(ind, categorical_dims, index_int_2_cat, number_dims):
            h_ind = {}

            for dim in categorical_dims:
                value = ind[dim]
                attr = categorical_dims[dim]
                h_ind[attr] = index_int_2_cat[attr][value]

            for dim in number_dims:
                value = ind[dim]
                attr = number_dims[dim]
                h_ind[attr] = value

            return h_ind

        def f_eval(ind, categorical_dims, index_int_2_cat, number_dims, iters, use_knowledge,
                   ml_model, t, upper_bound_knowledge):

            iters += 1
            try:
                h_ind = transform(ind, categorical_dims, index_int_2_cat, number_dims)
                utility = utility_function(attributes, weights_attr, values_attr, h_ind)
                diff = s - utility # (s - utility) * other_dealer_accept
                if use_knowledge and iters<upper_bound_knowledge:
                    x = Utils.convert_knowledge_to_sample_test(h_ind, t)
                    oponent_accepts = ml_model.predict([x])[0]
                    if oponent_accepts == 0:
                        return float("inf"),
                return diff,
            except:
                return float("inf"),

        def mutate(ind, values_attr, number_dims, categorical_dims):
            for i in range(len(ind)):
                mut = uniform(0, 1) <= prob_mutate
                if mut:
                    if i in number_dims:
                        if number_dims[i] in values_attr["integer"]:
                            ind[i] = randint(values_attr["integer"][number_dims[i]]["properties"]["min"],
                                             values_attr["integer"][number_dims[i]]["properties"]["max"])
                        else:
                            ind[i] = uniform(values_attr["integer"][number_dims[i]]["properties"]["min"],
                                             values_attr["integer"][number_dims[i]]["properties"]["max"])
                    else:
                        indexes = [i for i in range(len(values_attr["categorical"][categorical_dims[i]]["properties"]["choices"]))]
                        ind[i] = choice(indexes)
            return ind,

        def mate(ind_one, ind_two):
            a = [choice([ind_one[i], ind_two[i]]) for i in range(len(ind_one))]
            b = [choice([ind_one[i], ind_two[i]]) for i in range(len(ind_one))]
            return creator.Individual(a), creator.Individual(b)

        population      = []
        index_cat_2_int = {}
        index_int_2_cat = {}
        for attr in attributes:
            if attributes[attr] == "categorical":
                c = 0
                index_cat_2_int[attr] = {}
                index_int_2_cat[attr] = {}
                for pos_value in values_attr["categorical"][attr]["properties"]["choices"]:
                    index_cat_2_int[attr][pos_value] = c
                    index_int_2_cat[attr][c] = pos_value
                    c += 1

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        toolbox = base.Toolbox()

        categorical_dims = {}
        number_dims = {}
        for i in range(pob_size):
            individual = []
            d = 0
            e = 0
            for key in space:
                if space[key][0] == "integer":
                    individual.append(randint(int(space[key][1]), int(space[key][2] + 1)))
                    number_dims[e] = key
                elif space[key][0] == "categorical":
                    categorical_dims[d] = key
                    selected = choice(space[key][1])
                    int_selected = index_cat_2_int[key][selected]
                    individual.append(int_selected)
                d += 1
                e += 1
            population.append(creator.Individual(individual))

        toolbox.register("evaluate", f_eval, categorical_dims=categorical_dims,
                         index_int_2_cat=index_int_2_cat, number_dims=number_dims, iters=iters,
                         use_knowledge=use_knowledge, ml_model=ml_model, t=t,
                         upper_bound_knowledge=upper_bound_knowledge)

        toolbox.register("mate", mate)
        toolbox.register("mutate", mutate, values_attr=values_attr, number_dims=number_dims,
                         categorical_dims=categorical_dims)
        toolbox.register("select", tools.selTournament, tournsize=tournsize)
        hof = tools.ParetoFront()
        population, logbook = algorithms.eaSimple(population, toolbox, cxpb=prob_mating, mutpb=prob_mutate,
                                                          ngen=iterations, halloffame=hof, verbose=False)
        best = hof[0]
        best = transform(best, categorical_dims, index_int_2_cat, number_dims)
        best_utility = utility_function(attributes, weights_attr, values_attr, best)
        return best, best_utility

if __name__ == "__main__":
    """
    print(Offers.random_offer({"precio": ("integer", 10, 20),
                               "color": ("categorical", ["rojo", "verde", "azul"]),
                               "abs" : ("categorical", ["yes", "no"])
                               }))
    """
    Offers.genetic_offer({"precio": ("integer", 10, 20),
                         "hp" : ("integer", 75, 120)
                         })