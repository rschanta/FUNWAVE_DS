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
    print('\t\tStarted processing bathymetry...')
    
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

    # Update with new parameters
    output_vars['bathy_array'] = bathy_array
    output_vars['bathy_file'] = bathy_file
    output_vars['Mglob'] = Mglob

    print('\t\tSucessfully processed bathymetry...')
    return output_vars

'''
get_bathy_new()
    - second version of applying the bathymetry, used for D3e
'''
def get_bathy_new(vars):
    print('\t\tStarted processing bathymetry...')
    
    # Unpack Variables (note choice of bathy set by stability- get that later)
    bathyX = vars['bathyX']
    bathyh = vars['bathyh']
    WG_loc_x = vars['WG_loc_x']
    Xc_WK = vars['WG_loc_x']
    WG_to_use = vars['WG_to_use']
    pi_1 = vars['pi_1']
    MWL = vars['MWL']
    
    # Subtract mean of the MWL
    datum = np.nanmean(MWL)
    bathyZ = datum - bathyh

    # Get height needed for stability calcs
    h = bathyZ[0]
    vars['DEPTH_FLAT'] = h

    # Make a call to get_stability_vars, unpack DX and L
    output_vars = get_stability_vars(vars)
    DX = output_vars['DX']
    L = output_vars['L_']

    # Calculate the amount to add, if needed, and add on
    X_add = pi_1*L - WG_loc_x[WG_to_use]

    if X_add > 0:
        Xc_WK = Xc_WK + X_add
        bathyX = bathyX + X_add
    else:
        Xc_WK = WG_loc_x[WG_to_use]
        bathyX = bathyX
    
    # Add the propagation distance
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

    # Update with new parameters
    output_vars['bathy_array'] = bathy_array
    output_vars['bathy_file'] = bathy_file
    output_vars['Mglob'] = Mglob
    output_vars['Xc_WK'] = Xc_WK
    output_vars['X_add'] = X_add

    print('\t\tSucessfully processed bathymetry...')
    return output_vars