#!/usr/bin/env python3

import os
from steinertree.parser import parseSTP
from steinertree.solver import Solver
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

	
'''
	Runner
	
	This class builds and runs the GA to solve the steiner tree problem using the
	DEAP framework https://github.com/deap/deap

	you can find more information about DEAP in the notebooks at:
	https://github.com/DEAP/notebooks
	
	version: 0.2
	authors: Xiaoqian Xiong, Raoul Nicolodi, Martin Kaufleitner, Aurelien Hontabat
	license: MIT
'''

if not os.path.exists('plots'):
    os.makedirs('plots')

# Solve the Steiner Tree -------------------------------------------------------
# set the values for the GA
solver = Solver(mfitness = 500, psize = 20, cxpb = 0.9, mutpb = 0.05, tsize = 5, ngen = 100, componentCost = 20, mu=20)

# get the graph data
graph_data = parseSTP('./examples/data/B01.stp')

# evolve a solution
pop, log, hof = solver.solve(graph_data)


# Visualize Results ------------------------------------------------------------
gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
plt.plot(gen, avg, label="average")
plt.plot(gen, min_, label="minimum")
plt.plot(gen, max_, label="maximum")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(loc="lower right")
plt.savefig('./examples/plots/fitness.png')