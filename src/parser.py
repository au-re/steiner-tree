import numpy

# SECTION Graph 
# Nodes 50
# Edges 64
# E 2 3 5

# [(2,3,5)] numpy array


dtype = [('first', int), ('second', int), ('weight', int)]

def parse(filename):
    f = open(filename, 'r')
    graph_data = []
    terminals = numpy.zeros(0)
    for line in f:
        if line.startswith('Nodes '):
            terminals = numpy.zeros(int(line.split()[1]))
        if line.startswith('E '):
            arr = line.split()
            del arr[0]
            t = (int(arr[0]) - 1, int(arr[1]) - 1, int(arr[2]))
            graph_data.append(t)
        if line.startswith('T '):
            arr = line.split()
            terminals[int(arr[1]) - 1] = 1

    return numpy.array(graph_data, dtype=dtype), terminals
    

