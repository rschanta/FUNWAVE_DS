import numpy as np
from scipy.optimize import fsolve
from funwave_ds.fw_py.config_record import log_function_call
def get_stability_vars(vars):
    
    print('\t\tStarted applying variables dependent on stability...')
    # Unpack vars needed
    WKK = vars['WKK'] 
    h = vars['h']

    # Find wavelength (L) through linear dispersion root-finding
    sigma = 2 * np.pi / WKK.attrs.PeakPeriod
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

    print('\t\tFinished applying variables dependent on stability...')

    
    # Returning multiple variables and bonus variables
    return {'k_': k, 
        'L_': L,
        'kh': k*h,
        'DX': DX,
        'DY': DY}