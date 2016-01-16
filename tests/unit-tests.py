import numpy

def reassemble(modified_bits, fixed_bits):
    
    '''
        Reassembles the individual from the immutable bits and the bits that have 
        been modified. Takes two numpy arrays.
        
        Attributes
        modified_bits: the bits that have been changed during crossover. Should 
        have the length of the number of 0 in fixed_bits
        
        fixed_bits: bits that are not supposed to evolve
        
        Example
        reassemble(np.array([0,1,0]),np.array([1,0,0,0,1])) 
        -> [1,0,1,0,1]
        
    '''
    
    individual = numpy.zeros(fixed_bits.size)
    
    j = 0
    for i in range(fixed_bits.size):
        if fixed_bits[i] == 0:
            individual[i] = modified_bits[j]
            j+=1
        else:
            individual[i] = 1
    return individual
    
print('Reassembled individual', str(reassemble(numpy.array([0,1,0]),numpy.array([1,0,1,0,1]))))