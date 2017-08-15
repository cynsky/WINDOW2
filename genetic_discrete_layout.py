__author__ = 'Sebastian Sanchez Perez-Moreno. Email: s.sanchezperezmoreno@tudelft.nl'

from random import randint, random, choice
from fitness_for_optimisation import run_workflow
fitness = run_workflow
from memoize import Memoize2
fitness = Memoize2(fitness)
import time
from joblib import Parallel, delayed
from copy import deepcopy

result = open('gen_best_layout.dat', 'w', 1)
result2 = open('gen_fitness.dat', 'w', 1)
average = open('gen_average_fitness.dat', 'w', 1)
start_time = time.time()

id = []
x = []
y = []

with open("layout_grid.dat", "r") as grid:
    for line in grid:
        cols = line.split()
        x.append(float(cols[1]))
        y.append(float(cols[2]))
        id.append(int(cols[0]))


def change_duplicates(state):
    for ind in state:
        while len(ind) != len(set(ind)):
            ind2 = deepcopy(ind)
            sett = list(set(ind2))
            for num in sett:
                ind2.remove(num)
            for num in ind2:
                new = choice(id)
                while new in ind:
                    new = choice(id)
                ind[ind.index(num)] = new
        state[state.index(ind)] = ind
    return state


def vector_to_coordinates(v):
    coords = []
    for i in v:
        coords += [x[i]]
        coords += [y[i]]
    return coords


def make_vector(state, a):
    new = choice(id)
    while new in state:
        new = choice(id)
    state[a] = new
    return state


def gen_individual():
    state = [choice(id) for _ in range(9)]
    for a in range(len(state)):
        state = make_vector(state, a)
    return state


def gen_population(n_indiv):
    return [gen_individual() for _ in range(n_indiv)]


def grade_gen(b, n):
    average = 0.0
    for item in b:
        average += item / n
    return average


def optimise():
    n_iter = 20
    n_ind = 20
    mutation_rate = 0.01
    selection_percentage = 0.5
    random_selection = 0.05

    pops = gen_population(n_ind)
    n_ind = len(pops)

    for iteration in range(n_iter):  # Iteration through generations loop
        start_time2 = time.time()
        pop = deepcopy(pops)
        pops = []
        pop = change_duplicates(pop)
        # fit = Parallel(n_jobs=2)(delayed(fitness)(vector_to_coordinates(pop[i])) for i in range(n_ind))  # Parallel evaluation of fitness of all individuals
        fit = [fitness(vector_to_coordinates(pop[i])) for i in range(n_ind)]
        aver = grade_gen(fit, float(n_ind))
        print (aver)
        average.write('{}\n'.format(aver))

        fit = [[fit[i], i] for i in range(n_ind)]
        best_index = min(fit)[1]
        for xx in range(9):
            result.write('{}\t'.format(pop[best_index][xx]))  # This min implies minimisation.
        result.write('{}\n'.format(fit[int(best_index)][0]))

        for yy in range(n_ind):
            result2.write('{}\n'.format(fit[yy][0]))
        result2.write('\n')

        graded = [xx[1] for xx in sorted(fit, reverse=False)]

        retain_length = int(len(graded) * selection_percentage)
        parents_index = graded[:retain_length]

        # Add randomly other individuals for variety
        for item in graded[retain_length:]:
            if random_selection > random():
                parents_index.append(item)

        # Mutation of individuals
        for item in parents_index:
            if mutation_rate > random():
                a = randint(0, 8)
                state = pop[item]
                state = make_vector(state, a)
                pop[item] = state

        for item in parents_index:
            pops.append(pop[item])

        # Crossover function. Create children from parents
        parents_length = len(parents_index)
        desired_length = n_ind - parents_length
        children = []
        while len(children) < desired_length:
            parent1 = randint(0, parents_length - 1)
            parent2 = randint(0, parents_length - 1)
            if parent1 != parent2:
                parent1 = pop[parents_index[parent1]]
                parent2 = pop[parents_index[parent2]]
                cross_place = randint(0, 12)
                child = parent1[:cross_place] + parent2[cross_place:]
                children.append(child)
        pops.extend(children)

        print("%d iteration,--- %s seconds, --- best fitness: %f" % (iteration, time.time() - start_time2, fit[int(best_index)][0]))
    print("--- %s seconds ---" % (time.time() - start_time))
    with open("gen_layout_optimal.dat", "w") as output:
        for i in range(9):
            output.write("{} {}\n".format(x[pop[best_index][i]], y[pop[best_index][i]]))
    result.close()
    result2.close()
    average.close()

if __name__ == '__main__':
    # a = gen_individual()
    # print(a)
    # b = vector_to_coordinates(a)
    # print(b)
    # print(fitness(b))
    optimise()
