import numpy

#punishment for too many components
#BIG_VALUE = 100
#Treshold from which we subtract the weight, to obtain the fitness
#BIGGER_VALUE = 1000
'''
Should work now
'''
def root(a):
	if father[a] != a:
	    father[a] = root(father[a])
	return father[a]

def same(father, a, b):
	return root(a) == root(b)

father = numpy.arange(50)
'''
Calculates the Minimum spanning tree of the subgraph induced by the allowed vertices 
(=steiner vertices + starting points), used for the fitness evaluation  

I think it's best to represent the graph by a list of the edges, and they should be 
sorted before calling this method, as a matter of efficiency.
allowed_vertices is a bitstring, where 1 represents that the vertex should be in the MST and 0 that it doesnt

Uses Kruskal ad Union-Find datastructure with high compression to achieve almost linear complexity (n*Ack^(-1)(n,m))
'''
def mst(graph, tree_vertices):
    n = tree_vertices.size
    #father = numpy.arange(n)
    rank = numpy.zeros(n)
    cnt = 0
    for i in tree_vertices:
        cnt += i
    weight = 0
    #print(tree_vertices)
    #print(cnt)
    for edge in graph:
        a = edge[0]
        b = edge[1]
        rootA = root(a)
        rootB = root(b)
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
    return weight, cnt
    
def score(graph, tree_vertices, max_fitness, component_cost):
    weight, cnt = mst(graph, tree_vertices)
    fitness = (max_fitness - (weight + ((cnt - 1) * component_cost)))
    return fitness