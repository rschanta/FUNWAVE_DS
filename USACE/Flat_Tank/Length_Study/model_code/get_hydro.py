import pandas as pd
import numpy as np
from scipy.optimize import fsolve 
from scipy.optimize import brentq
def get_hydro(var_dict):
    # Unpack Variables-------------------------------------------------
    Tperiod = var_dict['Tperiod']
    DEPTH_FLAT = var_dict['DEPTH_FLAT']
    #-----------------------------------------------------------------
    print('\t\tStarted Calculating Hydrodynamic Variables...')


    
    def linear_dispersion_by_roots(T=None,
                                   h=None):
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
        k = brentq(disp_relation, 1e-12, 10)
        L = 2 * np.pi / k

        return k,L
    
    # Solve the dispersion relation, get wavelength
    k,L =  linear_dispersion_by_roots(T=Tperiod,
                                      h=DEPTH_FLAT)
    kh = k*DEPTH_FLAT

    # Return new parameters
    print('\t\tSuccessfully calculated hydrodynamic parameters!')
    return {'k': k,
            'L': L,
            'kh': kh}


