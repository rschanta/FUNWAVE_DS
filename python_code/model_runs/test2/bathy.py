import pickle
import os
import sys
import numpy as np
from scipy.interpolate import interp1d

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
import python_code as pc

## Give D3 Alt name
def set_alt_title(vars):
    trial_path = vars['bathy_path']
    return {'ALT_TITLE': os.path.splitext(os.path.basename(trial_path))[0]}

## Calculate stability for regular waves
def stability_vars(vars):
    # Unpack vars needed
    T = vars['Tperiod']
    h = vars['DEPTH_FLAT']
    k, L = pc.co.py.dispersion(T, h)
    
    # Use Torres stability limits for DX/DY amd Sponge
    DX_lo = h/15;
    DX_hi = L/60;
    DX = np.mean([DX_hi,DX_lo]);
    DY = DX
    Sponge_west_width = 2*L
    
    
    # Returning multiple variables and bonus variables
    return {'k_': k, 
            'L_': L,
            'DX': DX,
            'DY': DY,
            'Sponge_west_width': Sponge_west_width}

def get_bathy2(vars):
    data_path = vars['bathy_path']
    with open(data_path, 'rb') as f:
        try:
            bathy_raw = pickle.load(f)
        finally:
            f.close()  # Ensure the file is closed
        
    # Get variables needed
    bathy = bathy_raw['filtered_data']['bed_num_before']
    WG_x = bathy_raw['raw_data']['WG_loc_x']
    MWL = bathy_raw['raw_data']['MWL']
    bathyX = bathy[:,0]
    bathyh = bathy[:,1]
    
    L = vars['L_']
    DX = vars['DX']
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
    
    bathy_dict = {'bathy': bathy_out}
    
    return {'files': bathy_dict} 
