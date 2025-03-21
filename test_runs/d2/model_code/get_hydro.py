import numpy as np
from scipy.optimize import fsolve 

def get_hydro(var_dict):
    # Unpack Variables-------------------------------------------------
    Tperiod = var_dict['Tperiod']
    DEPTH_FLAT = var_dict['h_offshore']
    #-----------------------------------------------------------------
    print('\t\tStarted Calculating Hydrodynamic Variables...')

    # Parameters for dispersion relation
    sigma = 2 * np.pi / Tperiod
    g = 9.81
    h = DEPTH_FLAT
    
    # Dispersion relation to use
    def disp_relation(k):
        return sigma**2 - g * k * np.tanh(k * h)
    
    # Solve the dispersion relation, get wavelength
    k = fsolve(disp_relation, 0.1)[0]
    L = 2 * np.pi / k
    kh = k*h

    # Set beach_LS_width
    beach_LS_width = 1.25*L
    # Return
    print('\t\tSuccessfully calculated hydrodynamic parameters!')
    return {'k': k,
            'L': L,
            'kh': kh,
            'beach_LS_width':beach_LS_width}