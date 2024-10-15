import numpy as np
from scipy.optimize import fsolve
import pickle
def stability_vars(vars):
    # Unpack vars needed
    PeakPeriod = vars['PeakPeriod']
    pickle_file = vars['pickle_file']

    # Calculate height to use from data
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
        f.close()
    
    Hmo = data['filtered_data']['Hmo']

    # Extract data and MWL
    bathy = data['filtered_data']['bed_num_before']
    MWL = data['raw_data']['MWL']
    bathyX = bathy[:,0]
    bathyh = bathy[:,1]
    # Subtract mean of the MWL
    MWL_mean = np.nanmean(MWL)
    Z_raw = MWL_mean - bathyh
    h = Z_raw[0]
    
    # Find wavelength (L) through linear dispersion root-finding
    sigma = 2 * np.pi / PeakPeriod
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
    # Returning multiple variables and bonus variables
    return {'k_': k, 
        'L_': L,
        'DX': DX,
        'DY': DY,
        'bathyX': bathyX,
        'bathyZ': Z_raw,
        'Xc_WK': 0.0,
        'DEP_WK': h,
        'Sponge_west_width':0.0,
        'Hmo':Hmo}