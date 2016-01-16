import numpy


'''
	Parser
	functionality to parse stp data files
	
	version: 0.2
	authors: Xiaoqian Xiong, Raoul Nicolodi, Martin Kaufleitner, Aurelien Hontabat
	license: MIT
'''


dtype = [('first', int), ('second', int), ('weight', int)]


def parseSTP(filepath):
    '''
        Returns the graph data stored in an STP file given a filepath.
        
        Attributes
        filepath - path to the desired graph file
        
        Returns
        graph       - representation of the graph
        indsize     - the size of an individual
        fixedbits   - the bits of the graph that are immutable
    '''
    
    
    file        = open(filepath, 'r')
    graph_data  = []
    indsize     = 0
    fixedbits   = numpy.zeros(0)
    
    for line in file:
        if line.startswith('Nodes '):
            fixedbits = numpy.zeros(int(line.split()[1]))
        if line.startswith('E '):
            arr = line.split()
            del arr[0]
            t = (int(arr[0]) - 1, int(arr[1]) - 1, int(arr[2]))
            graph_data.append(t)
        if line.startswith('T '):
            arr = line.split()
            fixedbits[int(arr[1]) - 1] = 1
            
    
    graph = numpy.array(graph_data, dtype=dtype)
    graph = numpy.sort(graph, order='weight')
    
    # set the size of an individual for this graph a.k.a the number of zeros in 
    # the fixedbits
    for i in fixedbits:
        indsize += (1-i)
        indsize = int(indsize)

    return graph, indsize, fixedbits
	    

	    