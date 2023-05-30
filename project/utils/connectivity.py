import numpy as np
from scipy.sparse import csr_matrix
import scipy.stats as stats

def create_matrix(connection_type,num_neurons = 0, connection_fraction_e = 0.3, connection_fraction_c = 0.5,seed_ini = 1234 ):
    '''
    Creates a connectivity matrix, which characteristics can be defined while calling the function.

    Parameters:
        connection_type (str):
            'pair': there are only two neurons, connected between each other
            'electrical': electrical synapse matrix - symmetrical
            'chemical': chemical synapse matrix
        num_neurons (int, optional):
            the number of neurons of the network, default value is 0
        connection_fraction_e  (float, optional):
            the proportion of electrical synapses in the network, default value is 0.3
        connection_fraction_c (float, optional):
            the proportion of chemical synapses in the network, default value: 0.5
        seed_ini (int, optional):
            seed of the random number generator, default value 1234

    Returns:
        matrix (tuple[tuple[int,int]] | sparse_matrix):
            for 'pair' it returns an np.array. for the other cases, it resturns a sparse matrix that contains 1's representing connections between neurons.
        seed_ini (int):
            returns the seed used
    '''

    if connection_type == 'pair':
        matrix = np.array([ [0 , 1] ,[1, 0] ] )

    elif connection_type == 'electrical':
        np.random.seed(seed_ini)

        #Matrix of random numbers between 0 and 1. The heavyside function makes the variables either 0 or 1
        matrix = np.heaviside(connection_fraction_e - stats.uniform.rvs(size=(num_neurons,num_neurons)),0)

        #make the matrix symmetrical
        i_lower = np.tril_indices(len(matrix),-1)
        matrix[i_lower] = matrix.T[i_lower]

        #empty the diagonal
        np.fill_diagonal(matrix,0)
        matrix = csr_matrix(matrix)

    elif connection_type == 'chemical' : 
        np.random.seed(seed_ini + 37)

        #Matrix of random numbers between 0 and 1. The heavyside function makes the variables either 0 or 1
        matrix = np.heaviside(connection_fraction_c - stats.uniform.rvs(size=(num_neurons,num_neurons)),0)

        #remove the entries from the diagonal
        np.fill_diagonal(matrix,0)
        matrix = csr_matrix(matrix)

    return matrix, seed_ini