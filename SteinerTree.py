import random
import numpy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from fitness_calculator import score
from parser import *


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


# class for a complete parameter setting
class ParameterSetting:
	def __init__(self, maxFitIndiv, indSize, popSize, mateProb, mutateProb, tournSize, numGens, componentCost):
		self.maxFitIndiv = maxFitIndiv
		self.indSize = indSize
		self.popSize = popSize
		self.mateProb = mateProb
		self.mutateProb = mutateProb
		self.tournSize = tournSize
		self.numGens = numGens
		self.componentCost = componentCost


# Parameter settings
paramSetting = ParameterSetting(maxFitIndiv = 100, indSize = 2, popSize = 5, mateProb = 0.9, mutateProb = 0.05, tournSize = 3, numGens = 10, componentCost = 20)


#read in the graph and the terminal nodes
graph, allowed_vertices = parse()
#print(graph)


print('Graph: ', graph)
print('Allowed vertices: ', allowed_vertices)

graph = numpy.sort(graph, order='weight')

print('MST fitnessvalue', score(graph, allowed_vertices, paramSetting.maxFitIndiv, paramSetting.componentCost))    	
    	
    	

def reassemble(individual_part, vertices):
    
    # print('Reassemble called with ' +  str(individual_part) + ' ' + str(vertices))
    
    individual = numpy.zeros(vertices.size)
    j = 0
    
    for i in range(vertices.size):
        if vertices[i] == 0:
            individual[i] = individual_part[j]
            j+=1
        else:
            individual[i] = 1
            
    # print('Reassembled individual', str(individual))        

    return individual
		


# Type Creation
# I think this should be OK for us as well. We have individuals with a max fitness
# of 1.0
creator.create("FitnessMax", base.Fitness, weights=(paramSetting.maxFitIndiv,))
creator.create("Individual", list, fitness=creator.FitnessMax)


# Individual and Population
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, paramSetting.indSize)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# Evaluation Function
def evalBest(individual):
    
    print('individual', individual)
    print('best', score(graph, reassemble(individual, allowed_vertices), paramSetting.maxFitIndiv, paramSetting.componentCost))
    return score(graph, reassemble(individual, allowed_vertices), paramSetting.maxFitIndiv, paramSetting.componentCost),
    
#	return sum(individual), # don't forget the comma (returns tupple)


# Genetic Operators
toolbox.register("evaluate", evalBest)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=paramSetting.mutateProb)
toolbox.register("select", tools.selTournament, tournsize=paramSetting.tournSize)


# Evolving the Population

def main():
    
    pop = toolbox.population(n=paramSetting.popSize)
    print('population:', pop)
    
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=paramSetting.mateProb, mutpb=paramSetting.mutateProb, ngen=paramSetting.numGens, stats=stats, halloffame=hof, verbose=True)
    
    return pop, logbook, hof


# Visualize Results

pop, log, hof = main()
print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

# print('fitnessfunction individual [1,0,0,1]', mst(graph, [1,0,0,1]))
# print('fitnessfunction individual [1,1,1,1]', mst(graph,  [1,1,1,1]))
# print('fitnessfunction individual [1,0,1,1]', mst(graph, [1,0,1,1]))
# print('fitnessfunction individual [1,1,0,1]', mst(graph, [1,1,0,1]))

# gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
# plt.plot(gen, avg, label="average")
# plt.plot(gen, min_, label="minimum")
# plt.plot(gen, max_, label="maximum")
# plt.xlabel("Generation")
# plt.ylabel("Fitness")
# plt.legend(loc="lower right")
# plt.savefig('fitness.png')


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
