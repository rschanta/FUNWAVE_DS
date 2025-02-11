'''
Code for various linear dispersion calculations
'''

import numpy as np
from scipy.optimize import fsolve



def linear_dispersion_by_roots(T,h):
    '''
    Solve the linear dispersion relation given period `T` and depth `h`
    using iterative root finding
    '''
    # Define orbital period
    sigma = 2 * np.pi / T
    # Define gravity
    g = 9.81

    # Definition of the linear dispersion relation
    def disp_relation(k):
        return sigma**2 - g * k * np.tanh(k * h)
    
    # Linear root finding
    k = fsolve(disp_relation, 1)[0]
    L = 2 * np.pi / k

    return k,L
