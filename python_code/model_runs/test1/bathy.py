import copy
import pickle
import numpy as np
import sys
from itertools import product
import python_code as fp
from scipy.interpolate import interp1d

def prep_D3_bathy_trial_5(trial_dict,DX,L):
    # Get variables needed
    bathy = trial_dict['filtered_data']['bed_num_before']
    WG_x = trial_dict['raw_data']['WG_loc_x']
    MWL = trial_dict['raw_data']['MWL']
    bathyX = bathy[:,0]
    bathyh = bathy[:,1]

    # Add propagation room
    bathyX = bathyX + 3*L
    bathyX = np.insert(bathyX, 0, 0)
    bathyh = np.insert(bathyh, 0, bathyh[0])

    # Convert to depth values
    MWL_mean = np.nanmean(MWL)
    Z_raw = MWL_mean - bathyh
    
    # Interpolate values
    X_out = np.arange(0, np.max(bathyX)+0.1, DX)
    f = interp1d(bathyX, Z_raw, kind='linear', fill_value="extrapolate")
    Z_out = f(X_out)
    
    # Arrange outputs
    bathy_out = {}
    bathy_out['array'] = np.stack((X_out, Z_out), axis=1)
    bathy_out['file'] = np.stack((Z_out,Z_out,Z_out),axis=0)
    bathy_out['WG_x'] = WG_x
    
    return bathy_out

def get_stability_limits(trial_dict,peak_period):
    # Get depth
    bathy = trial_dict['filtered_data']['bed_num_before']
    MWL = trial_dict['raw_data']['MWL']
    Xc_WK = bathy[0,0]
    bathyh = bathy[:,1]
    MWL_mean = np.nanmean(MWL)
    h = MWL_mean - bathyh[0];
    
    # Calculate dispersion relation
    k, L = fp.py.dispersion(peak_period, h)
    
    # DX Limits
    DX_lo = h/15;
    DX_hi = L/60;
    DX = np.mean([DX_hi,DX_lo]);
    
    return L, DX, h, Xc_WK