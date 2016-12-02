from random import randint, uniform, choice
from deap import base, creator, tools, algorithms
from Utility import Utility

class Offers:

    # space = {(attr_1, space_1), (attr_2, space_2), ...,(attr_n, space_n) : space_i \in {(int, min, max), (float, min, max), (str, list)}} #
    @staticmethod
    def random_offer(space, s, utility_function, attributes, weights_attr, values_attr):
        act_s = 0
        while act_s<s:
            res = {}
            for key in space:
                if space[key][0]=="integer": res[key] = randint(int(space[key][1]), int(space[key][2]+1))
                elif space[key][0]=="float": res[key] = uniform(space[key][1], space[key][2]+1)
                elif space[key][0]=="categorical": res[key] = choice(space[key][1])
            act_s = utility_function(attributes, weights_attr, values_attr, res)
        return res, act_s

    # Only with int attributes #
    @staticmethod
    def genetic_offer(space, s, utility_function, attributes, weights_attr, values_attr, pob_size=50,
                      prob_mutate=0.01, prob_mating=0.4, iterations=10, tournsize=3):

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

        def f_eval(ind, categorical_dims, index_int_2_cat, number_dims):
            try:
                h_ind = transform(ind, categorical_dims, index_int_2_cat, number_dims)
                utility = utility_function(attributes, weights_attr, values_attr, h_ind)
                diff = abs(s - utility)
                if diff<0 or 1<diff: return float("inf"),
                return diff,
            except:
                return float("inf"),

        def mutate(ind):
            for i in range(len(ind)-1):
                mut = uniform(0, 1) <= prob_mutate
                rand_pos = randint(0, len(ind)-1)
                if mut: ind[rand_pos], ind[i] = ind[i], ind[rand_pos]
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


        toolbox.register("evaluate", f_eval, categorical_dims=categorical_dims, index_int_2_cat=index_int_2_cat, number_dims=number_dims)
        toolbox.register("mate", mate)
        toolbox.register("mutate", mutate)
        toolbox.register("select", tools.selTournament, tournsize=tournsize)
        hof = tools.ParetoFront()
        population, logbook = algorithms.eaSimple(population, toolbox, cxpb=prob_mating, mutpb=prob_mutate,
                                                      ngen=iterations, halloffame=hof)
        return transform(hof[0], categorical_dims, index_int_2_cat, number_dims), \
               f_eval(hof[0], categorical_dims, index_int_2_cat, number_dims )

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