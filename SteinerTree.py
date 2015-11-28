import random
import numpy
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms


'''
	SteinerTree
	
	Code scaffold for solving the SteinerTree problem using the
	DEAP framework https://github.com/deap/deap
	(currently OneMax problem)
	
	you can find more information about DEAP in the notebooks at:
	https://github.com/DEAP/notebooks
	
	version: 0.1
	authors: Xiaoqian Xiong, Raoul Nicolodi, Martin Kaufleitner, Aurelien Hontabat
	license: MIT
'''


# Type Creation

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


# Individual and Population

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# Evaluation Function

def evalOneMax(individual):
	return sum(individual), # don't forget the comma (returns tupple)


# Genetic Operators

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


# Evolving the Population

def main():
    
    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, stats=stats, halloffame=hof, verbose=True)
    
    return pop, logbook, hof


# Visualize Results

pop, log, hof = main()
print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
plt.plot(gen, avg, label="average")
plt.plot(gen, min_, label="minimum")
plt.plot(gen, max_, label="maximum")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(loc="lower right")


# Alternative: defining the generation step process

# population = toolbox.population(n=300)
# NGEN=40
# 
# for gen in range(NGEN):
# 	
# 	offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
# 	fits = toolbox.map(toolbox.evaluate, offspring)
# 	
# 	for fit, ind in zip(fits,offspring):
# 		ind.fitness.values = fit
#
# 	population = toolbox.select(offspring, k=len(population))
# 	
# top10 = tools.selBest(population, k=10)
# 
# print(top10)
