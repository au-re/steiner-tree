import numpy

#punishment for too many components
#BIG_VALUE = 100
#Treshold from which we subtract the weight, to obtain the fitness
#BIGGER_VALUE = 1000
'''
Should work now
'''
def root(father, a):
	if father[a] != a:
	    father[a] = root(father, father[a])
	return father[a]

def same(father, a, b):
	return root(father, a) == root(father, b)

'''
Calculates the Minimum spanning tree of the subgraph induced by the allowed vertices 
(=steiner vertices + starting points), used for the fitness evaluation  

I think it's best to represent the graph by a list of the edges, and they should be 
sorted before calling this method, as a matter of efficiency.
allowed_vertices is a bitstring, where 1 represents that the vertex should be in the MST and 0 that it doesnt

Uses Kruskal ad Union-Find datastructure with high compression to achieve almost linear complexity (n*Ack^(-1)(n,m))
'''
def mst(steinergraph, tree_vertices):
    #print('entering mst with tree_vertices: ', tree_vertices)
    graph = steinergraph.edges
    n = tree_vertices.size
    father = numpy.arange(n)
    #father = numpy.arange(n)
    rank = numpy.zeros(n)
    cnt = 0
    for i in tree_vertices:
        cnt += i
    #print('initial cnt: ', cnt)
    weight = 0
    #print(tree_vertices)
    #print(cnt)
    for edge in graph:
        a = edge[0]
        b = edge[1]
        rootA = root(father, a)
        rootB = root(father, b)
        if tree_vertices[a] and tree_vertices[b] and rootA != rootB:
            weight += edge[2]
            if rank[rootA] > rank[rootB]:
                father[rootB] = rootA
            else:
                if rank[rootA] < rank[rootB]:
                    father[rootA] = rootB
                else:
                    father[rootA] = rootB
                    rank[rootB] += 1
            cnt -= 1
    '''
    print('Weight:', weight)
    print('Count:', cnt)
    print('Treevert', tree_vertices) 
    print('Fitness:', fitness)
    '''
    #print('leaving mst with weight: ', weight, ' and cnt: ', cnt)
    return weight, cnt
    
def score(graph, tree_vertices, max_fitness, component_cost):
    weight, cnt = mst(graph, tree_vertices)
    fitness = (max_fitness - (weight + ((cnt - 1) * component_cost)))
    return fitness