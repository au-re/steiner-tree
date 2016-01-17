#!/usr/bin/env python3

import os, sys, re
from steinertree.parser import parseSTP
from steinertree.solver import Solver
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import numpy #remove

	
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

# Import Graph -----------------------------------------------------------------
# pass an stp file as argument
if(len(sys.argv) != 2):
	print('''Please provide the relative path of the graph as argument 
Example: \'python run.py example.stp\'''')
	sys.exit(0)

# check if the file exists and stores the data in memory
try:
	# get the graph data
	graph_data = parseSTP(sys.argv[1])
except IOError:
	print('''The path provided doesn't match any valid document''')
	sys.exit(0)

# save file names to use for exports
fn = re.compile('[^/]+(?=\.stp)')
filename = str(fn.search(sys.argv[1]).group())


if not os.path.exists('plots'):
    os.makedirs('plots')

# Solve the Steiner Tree -------------------------------------------------------
# set the values for the GA
solver = Solver(mfitness = 500, psize = 20, cxpb = 0.9, mutpb = 0.05, tsize = 5, ngen = 100, componentCost = 20, mu=20)

# evolve a solution
pop, log, hof = solver.solve(graph_data)

# Visualize Results ------------------------------------------------------------
print('Best performing individual:', hof[0])
#print(graph_data[0])

# plot fitness improvement over generations
gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
plt.plot(gen, avg, label="average")
plt.plot(gen, min_, label="minimum")
plt.plot(gen, max_, label="maximum")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(loc="lower right")
plt.savefig('./plots/' + filename + '_fitness.png')
plt.clf()


# TODO move this
def reassemble(modifiedbits, fixedbits):
	
	individual = numpy.zeros(fixedbits.size)
	
	j = 0
	for i in range(fixedbits.size):
	    if fixedbits[i] == 0:
	        individual[i] = modifiedbits[j]
	        j+=1
	    else:
	        individual[i] = 1
	return individual
	
# visualize any graph with connections (assume all edges between active nodes are connected)
def visualizeGraph(individual, edges, fixedbits):
	
	G=nx.Graph()
	
	# get the possible edges of the graph
	for i in range(len(edges)):
		n1, n2, w = edges[i]
		G.add_edge(str(n1),str(n2), weight = w)
	
	
	# the nodes of the graph (differenciate between fixed and non-fixed nodes)
	fixed_nodes = [m for (m) in G.nodes() if fixedbits[int(m)] == 1]
	optional_nodes = [m for (m) in G.nodes() if fixedbits[int(m)] == 0]
	
	
	# selected nodes by the algorithm
	selected_nodes = [m for m in G.nodes() if reassemble(individual, fixedbits)[int(m)] == 1 and fixedbits[int(m)] == 0]


	# positions for all nodes
	pos=nx.spring_layout(G, k=1, scale=8) 
	
	
	# nodes
	nx.draw_networkx_nodes(G,pos,node_size=120, node_color='#32CD32', nodelist=fixed_nodes)
	nx.draw_networkx_nodes(G,pos,node_size=80, node_color='#dddddd', nodelist=optional_nodes)
	nx.draw_networkx_nodes(G,pos,node_size=100, node_color='#ADD8E6', nodelist=selected_nodes)
	
	
	# edges
	auto_selected_edges = [(u,v,w) for (u,v,w) in G.edges(data=True) if u in fixed_nodes and v in fixed_nodes]
	selected_edges = [(u,v,w) for (u,v,w) in G.edges(data=True) if (u in selected_nodes or u in fixed_nodes) and (v in selected_nodes or v in fixed_nodes)]

	
	nx.draw_networkx_edges(G,pos,edgelist=G.edges(), width=0.5, edge_color='#eeeeee')
	nx.draw_networkx_edges(G,pos,edgelist=auto_selected_edges, width=1, edge_color='#32CD32')
	nx.draw_networkx_edges(G,pos,edgelist=selected_edges, width=1, edge_color='#ADD8E6')

	
	# labels
	nx.draw_networkx_labels(G,pos,font_size=8,font_family='sans-serif')
	plt.axis('off')
	plt.savefig("./plots/" + filename + "_weighted_graph.png") # save as png
	plt.clf()
	
	# TODO: add information to the plot (gen num,...)

visualizeGraph(hof[0], edges=graph_data[0], fixedbits=graph_data[2])
	
print('Graph generated')
	
