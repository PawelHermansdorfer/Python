from pyeasyga import pyeasyga
import numpy as np
import random


data = [50, 50,   # x0 y0
        100, 100] # x1 y1
expected = [75, 75, 25]

ga = pyeasyga.GeneticAlgorithm(data,
                               population_size=50,
                               generations=100,
                               crossover_probability=0.8,
                               mutation_probability=0.05,
                               elitism=True,
                               maximise_fitness=True)

def create_individual(data):
    w = data[2] - data[0]
    h = data[3] - data[1]
    return [random.uniform(data[0], data[2]), 
            random.uniform(data[1], data[3]), 
            random.uniform(0, max(w, h))]
ga.create_individual = create_individual

def fitness_1(individual, data):
    cx, cy, r = individual
    x0, y0, x1, y1 = data[0], data[1], data[2], data[3]
    center_x_fitness = -abs(cx - (x0+(x1 - x0)/2))
    center_y_fitness = -abs(cy - (x0+(y1 - y0)/2))
    r_fitness        = -abs(r - max(x1 - x0, y1 - y0)/2)
    return center_x_fitness + center_y_fitness + r_fitness

def fitness_2(individual, data):
    cx, cy, r = individual
    x0, y0, x1, y1 = data[0], data[1], data[2], data[3]
    return r - 10*(abs((x0+(x1-x0)/2) - cx) - 10*abs((y0+(y1-y0)/2) - cy))
    
def chatgp_fitness(individual, data):
    cx, cy, r = individual
    x0, y0, x1, y1 = data[0], data[1], data[2], data[3]
    penalty = 0
    penalty_multiplier = 1000
    penalty += max(0, x0 + r - cx) * penalty_multiplier
    penalty += max(0, cx - (x1 - r)) * penalty_multiplier
    penalty += max(0, y0 + r - cy) * penalty_multiplier
    penalty += max(0, cy - (y1 - r)) * penalty_multiplier
    return r - penalty

for fitness_proc in [fitness_1, fitness_2, chatgp_fitness]:
    ga.fitness_function = fitness_proc

    cx_errors = []
    cy_errors = []
    r_errors  = []
    for i in range(10):
        ga.run()
        fitness, individual = ga.best_individual()
        cx_errors.append(abs(expected[0] - individual[0]))
        cy_errors.append(abs(expected[1] - individual[1]))
        r_errors.append(abs(expected[2] - individual[2]))

    result = '''{}
    mean cx error: {:.2f}
    mean cy error: {:.2f}
    mean r  error: {:.2f}'''.format(fitness_proc.__name__, np.mean(cx_errors), np.mean(cy_errors), np.mean(r_errors))
    print(result)
