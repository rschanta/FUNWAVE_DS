import numpy as np
from scipy.optimize import brentq



def get_hydro(var_dict):
    
    h = var_dict['MWL_left']
    T = var_dict['PeakPeriod']
    sigma = 2*np.pi/T
    
    # Define gravity
    g = 9.81
    
    
    # Definition of the linear dispersion relation
    def disp_relation(k):
        return sigma**2 - g * k * np.tanh(k * h)
 
    # Linear root finding
    k = brentq(disp_relation, 1e-12, 10)
    L = 2 * np.pi / k
    
    return {'k': k,
            'L': L,
            'kh': k*h}
