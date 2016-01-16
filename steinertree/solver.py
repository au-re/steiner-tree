import random
import numpy
from deap import base, creator, tools, algorithms
from steinertree.fitness import score, mst


'''
    Solver
    
    This class builds the GA to solve the steiner tree problem using the
    DEAP framework https://github.com/deap/deap

    you can find more information about DEAP in the notebooks at:
    https://github.com/DEAP/notebooks
    
    version: 0.2
    authors: Xiaoqian Xiong, Raoul Nicolodi, Martin Kaufleitner, Aurelien Hontabat
    license: MIT
'''


class Solver:
    
    def __init__(self, mfitness, psize, cxpb, mutpb, tsize, ngen, componentCost, mu):
        '''
            Solver object containing all the settings for the GA
        
            Attributes
            mfitness    - maximal fitness for an individual
            psize       - population size
            cxpb        - crossover/mating probability
            mutpb       - mutation probability
            tsize       - size of the tournament (pool for selection of best individual)
            ngen        - number of generations
            componentCost - cost of adding connections
            mu          - 
        
        '''
        
        # 
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)
    
        #
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_bool", random.randint, 0, 1)
        self.toolbox.register("mate", tools.cxTwoPoint)
        
        # setting up the GA 
        self.setup(mfitness, psize, cxpb, mutpb, tsize, ngen, componentCost, mu)

        

        
    def setup(self, mfitness, psize, cxpb, mutpb, tsize, ngen, componentCost, mu):
        ''' 
            enables to externally reset the attributes of the GA for fast prototyping
            
        '''
        
        self.mfitness       = mfitness
        self.psize          = psize        
        self.cxpb           = cxpb
        self.mutpb          = mutpb
        self.tsize          = tsize
        self.ngen           = ngen
        self.componentCost  = componentCost
        self.mu             = mu
        self.indsize        = 0
        
        # setup the max fitness for an individual and its base structure 
        creator.create("FitnessMax", base.Fitness, weights=(self.mfitness,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        # setup the framework with out evaluation, mutation and selection function
        self.toolbox.register("evaluate", self._evalInd)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=self.mutpb)
        self.toolbox.register("select", tools.selTournament, tournsize=self.tsize)
    
    
    def _reassemble(self, modifiedbits, fixedbits):
        '''
            Reassembles the individual from the immutable bits and the bits that have 
            been modified during the crossover. Takes two numpy arrays.
            
            Attributes
            modifiedbits - the bits that have been changed during crossover. Should 
            have the length of the number of 0 in fixedbits
            
            fixedbits - bits that are not supposed to evolve
            
            Example
            reassemble(np.array([0,1,0]),np.array([1,0,0,0,1])) -> [1,0,1,0,1]
            
        '''
        
        individual = numpy.zeros(fixedbits.size)
        
        j = 0
        for i in range(fixedbits.size):
            if fixedbits[i] == 0:
                individual[i] = modifiedbits[j]
                j+=1
            else:
                individual[i] = 1
        return individual
        

    
    def _evalInd(self, indbits):
        '''
            Evaluates the fitness of an individual. Wrapper to connect the score 
            function in 'fitness.py' to the framework. Returns the fitness of the 
            individual.
            
            Attributes
            indbits - the bits of an individual that have been crossed over
            
        '''
        
        # reassemble the individual 
        individual = self._reassemble(indbits, self.fixedbits)
        
        return score(self.graph, individual, self.mfitness, self.componentCost)


    def solve(self, graph_data):
        '''
            Given the graph data of a specific graph, runs the GA on it. 
            In this case it is the ... from the DEAP framework. Returns the 
            and the individuals from the hall of fame.
            
            Attributes
            graph_data - the data parsed from the STP file
            
        '''
        
        print(self.mfitness)
        
        self.graph, self.indsize, self.fixedbits  = graph_data

        # functions for initiating the individuals and the population with random bits
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, self.indsize)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        # setup hall of fame and generate the population
        hof             = tools.HallOfFame(10)
        population      = self.toolbox.population(n=self.psize)
        
        print(self.toolbox.population(1))
        
        
        pop, logbook    = algorithms.eaMuPlusLambda(population, 
                                                    self.toolbox, 
                                                    lambda_ = self.psize, 
                                                    mu      = self.mu, 
                                                    cxpb    = self.cxpb, 
                                                    mutpb   = self.mutpb, 
                                                    ngen    = self.ngen, 
                                                    stats   = self.stats, 
                                                    halloffame = hof, 
                                                    verbose = True)
        
        return pop, logbook, hof
