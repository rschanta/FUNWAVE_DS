import copy
import pickle
import numpy as np
import sys
from itertools import product
sys.path.append(r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Local Workspace\Python-6')
import funwave_py as fp
from scipy.interpolate import interp1d

def prep_D3_bathy_trial_5(trial_dict,DX):
    # Get variables needed
    bathy = trial_dict['filtered_data']['bed_num_before']
    WG_x = trial_dict['raw_data']['WG_loc_x']
    MWL = trial_dict['raw_data']['MWL']
    bathyX = bathy[:,0]
    bathyh = bathy[:,1]

    # Convert to depth values
    MWL_mean = np.nanmean(MWL)
    Z_raw = MWL_mean - bathyh;
    
    # Interpolate values
    X_out = np.arange(0, np.max(bathyX)+0.001, DX)
    f = interp1d(bathyX, Z_raw, kind='linear')
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
    k, L = fp.dispersion(peak_period, h)
    
    # DX Limits
    DX_lo = h/15;
    DX_hi = L/60;
    DX = np.mean([DX_hi,DX_lo]);
    
    return L, DX, h, Xc_WK