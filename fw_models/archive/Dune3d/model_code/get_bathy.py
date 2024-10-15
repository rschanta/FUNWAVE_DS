'''
get_bathy
    - Prepare the bathymetry from Dune3 data
    - Also makes a call to get_stability vars to determine
        optimal grid spacing based on wavelengths
'''


import numpy as np
from .get_stability import get_stability_vars

'''
get_bathy()
    - first version of applying the bathymetry, used for T1
'''
def get_bathy(vars):
    print('\tStarted processing bathymetry...')
    
    # Unpack Variables (note choice of bathy set by stability- get that later)
    bathyX = vars['bathyX']
    bathyh = vars['bathyh']
    pi_1 = vars['pi_1']
    MWL = vars['MWL']
    
    # Subtract mean of the MWL
    MWL_mean = np.nanmean(MWL)
    bathyZ = MWL_mean - bathyh

    # Get height needed for stability calcs
    h = bathyZ[0]
    vars['DEPTH_FLAT'] = h

    # Make a call to get_stability_vars, unpack DX and L
    output_vars = get_stability_vars(vars)
    DX = output_vars['DX']
    L = output_vars['L_']

    # Add on the amount specified by pi_1
    bathyX += pi_1*L
    bathyX = np.insert(bathyX, 0, 0)
    bathyZ = np.insert(bathyZ, 0, bathyZ[0])
    
    # Remove duplicate X values (issue for some trials, also from pi_1=0)
    unique_X, indices = np.unique(bathyX, return_index=True)
    sorted_indices = np.sort(indices)
    bathyX = bathyX[sorted_indices]
    bathyZ = bathyZ[sorted_indices]

    # Interpolate to grid
    X_out = np.arange(0, np.max(bathyX) + DX, DX)
    Z_out = np.interp(X_out, bathyX, bathyZ)

    # Get Mglob
    Mglob = int(len(X_out))

    # Prepare outputs
    bathy_array = np.column_stack((X_out, Z_out))
    bathy_file = np.tile(Z_out, (3, 1))

    # Bathy Dictionary
    bathy = {'array': bathy_array,
            'file': bathy_file}

    # Update with new parameters
    output_vars['bathy'] = bathy
    output_vars['Mglob'] = Mglob

    print('\tSucessfully processed bathymetry...')
    return output_vars