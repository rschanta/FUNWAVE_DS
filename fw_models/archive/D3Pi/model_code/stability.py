import numpy as np
from scipy.optimize import fsolve
import pickle
def get_stability_vars(vars):
    print('\tStarted applying variables dependent on stability...')
    # Unpack vars needed
    Tperiod = vars['Tperiod']
    h = vars['DEPTH_FLAT']

    # Find wavelength (L) through linear dispersion root-finding
    sigma = 2 * np.pi / Tperiod
    g = 9.81
    def disp_relation(k):
        return sigma**2 - g * k * np.tanh(k * h)
    k = fsolve(disp_relation, 0)[0]
    L = 2 * np.pi / k

    # Use Torres stability limits for DX/DY amd Sponge
    DX_lo = h/15
    DX_hi = L/60
    DX = np.mean([DX_hi,DX_lo])
    DY = DX

    # Set DEP_WK to DEPTH_FLAT as well
    DEP_WK = h
    print('\tFinished applying variables dependent on stability...')
    # Returning multiple variables and bonus variables
    return {'k_': k, 
        'L_': L,
        'kh': k*h,
        'DX': DX,
        'DY': DY,
        'DEP_WK': h}