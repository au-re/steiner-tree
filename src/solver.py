import random
import numpy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
#Our score function and parser
from fitness_calculator import score, mst
from parser import *
from selection import *

'''
	SteinerTree
	
	Code scaffold for solving the SteinerTree problem using the
	DEAP framework https://github.com/deap/deap

	you can find more information about DEAP in the notebooks at:
	https://github.com/DEAP/notebooks
	
	version: 0.1
	authors: Xiaoqian Xiong, Raoul Nicolodi, Martin Kaufleitner, Aurelien Hontabat
	license: MIT
'''

# class for a complete parameter setting
class ParameterSetting:
	def __init__(self, maxFitIndiv, popSize, mateProb, mutateProb, tournSize, numGens, componentCost, mu, hofSize, number_of_runs, verbose, crossoverFunction, mutationFunction):
		self.maxFitIndiv = maxFitIndiv
		self.popSize = popSize
		self.mateProb = mateProb
		self.mutateProb = mutateProb 
		self.tournSize = tournSize
		self.numGens = numGens
		self.componentCost = componentCost
		self.mu = mu
		self.hofSize = hofSize
		self.verbose = verbose
		self.number_of_runs = number_of_runs
		self.crossoverFunction = crossoverFunction
		self.mutationFunction = mutationFunction
	def __str__(self):
	    return "Maximal Fitness of an Individual: %d\nPopulation Size: %d\nCrossover Probability: %f\nMutation Probability: %f\nTournament Size: %f\nNumber of Generations: %d\nComponent Cost: %d\nMu: %d\nHall of Fame Size: %d\nVerbose: %s\nNumber of runs: %d\nCrossover Function: %s\nMutation Function: %s\n" % (self.maxFitIndiv, self.popSize, self.mateProb, self.mutateProb, self.tournSize,self.numGens, self.componentCost, self.mu, self.hofSize, self.verbose, self.number_of_runs, self.crossoverFunction, self.mutationFunction)
	    
class SteinerInstance:
    def __init__(self, filename):
        edges, allowed_vertices = parse(filename)
        indSize = 0
        for i in allowed_vertices:
            indSize += (1-i)
        indSize = int(indSize)
        #print('Graph: ', graph)
        #print('Allowed vertices: ', allowed_vertices)

        edges = numpy.sort(edges, order='weight')
        
        self.edges = edges
        self.allowed_vertices = allowed_vertices
        self.indSize = indSize

        #print('MST fitnessvalue', score(graph, allowed_vertices, paramSetting.maxFitIndiv, paramSetting.componentCost))    	
    def __str__(self):
        return 'edges: %s\nallowed_vertices: %s\nindSize: %s\n' % (self.edges, self.allowed_vertices, self.indSize)

class SteinerTreeSolver:
    def __init__(self, paramSetting):
        self.paramSetting = paramSetting
        creator.create("FitnessMax", base.Fitness, weights=(paramSetting.maxFitIndiv,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox = self.setup_toolbox()
        self.stats = self.setup_stats()
        self.graph = None
        # Type Creation
        # I think this should be OK for us as well. We have individuals with a max fitness
        # of 1.0
    
    def setup_toolbox(self):
        # Individual and Population
        toolbox = base.Toolbox()
        toolbox.register("attr_bool", random.randint, 0, 1)
        # Genetic Operators
        toolbox.register("evaluate", self.evaluate)
        #toolbox.register("mate", TwoPointCrossover)
        toolbox.register("mate", self.paramSetting.crossoverFunction)
        toolbox.register("mutate", self.paramSetting.mutationFunction, prob=self.paramSetting.mutateProb)
        toolbox.register("select", tools.selTournament, tournsize=self.paramSetting.tournSize)
        #toolbox.register("select", tools.selRoulette)
        return toolbox
        
    def setup_stats(self):
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        return stats
        
    def reassemble(self, individual_part, vertices):
        #print('Reassemble called with ' +  str(individual_part) + ' ' + str(vertices))
        individual = numpy.zeros(vertices.size)
        j = 0
        for i in range(vertices.size):
            if vertices[i] == 0:
                individual[i] = individual_part[j]
                j+=1
            else:
                individual[i] = 1
        #print('Reassembled individual', str(individual))
        return individual
    
    # Evaluation Function
    def evaluate(self, individual):
        #print('\nindividual:', individual)
        individual_score = score(self.graph, self.reassemble(individual, self.graph.allowed_vertices), self.paramSetting.maxFitIndiv, self.paramSetting.componentCost)
        #print('score: ', individual_score)
        return individual_score,
    
    def solve(self, graph, output_stats = False, output_plot = False, filename = None):
        self.graph = graph
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, graph.indSize)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        pop = self.toolbox.population(n=self.paramSetting.popSize)
        hof = tools.HallOfFame(self.paramSetting.hofSize)
        #print('initial_population:', pop)
        #pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=paramSetting.mateProb, mutpb=paramSetting.mutateProb, ngen=paramSetting.numGens, stats=stats, halloffame=hof, verbose=True)
        pop, logbook = algorithms.eaMuPlusLambda(pop, self.toolbox, lambda_=self.paramSetting.popSize, mu=self.paramSetting.mu, cxpb=self.paramSetting.mateProb, mutpb=self.paramSetting.mutateProb, ngen=self.paramSetting.numGens, stats=self.stats, halloffame=hof, verbose = self.paramSetting.verbose)
        
        if output_plot:
            gen, avg, min_, max_ = logbook.select("gen", "avg", "min", "max")
            plt.plot(gen, avg, label="average")
            plt.plot(gen, min_, label="minimum")
            plt.plot(gen, max_, label="maximum")
            plt.xlabel("Generation")
            plt.ylabel("Fitness")
            plt.legend(loc="lower right")
            plt.savefig(filename)
            plt.close()
        
        if output_stats:
            return pop, hof
        return pop
    
#print("Best individual is: %s\nwith fitness: %s. \nIt's spanning forest has a weight of %s \nand consists of %s components." % (hof[0], hof[0].fitness, weight, cnt))

#Alternative: defining the generation step process

#population = toolbox.population(n=300)
#NGEN=40
 
#for gen in range(NGEN):
	
#	offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
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
