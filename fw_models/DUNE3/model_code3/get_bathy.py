import numpy as np
from .get_stability import get_stability_vars
from funwave_ds.fw_py.config_record import log_function_call

'''
get_bathy_new()
    - second version of applying the bathymetry, used for D3e
'''
def get_bathy(vars):
    print('\t\tStarted processing bathymetry...')
    
    # Unpack Variables (note choice of bathy set by stability- get that later)
    XR = vars['XR']                     # Raw X positions
    XF = vars['XF']                     # Filtered X positions
    HR = vars['HR']                     # Raw bathymetry heights from bottom of flume
    HF = vars['HF']                     # Filtered bathymetry heights from bottom of flume
    WGR = vars['WGR']                   # Raw poisition of the wave gauges in X
    WGF = vars['WGF']                   # Filtered position of the wave gauges in X
    MWLR = vars['MWLR']                 # Raw MWL at wave gauges

    
    WG_to_use = vars['WG_to_use']       # spectra position to use
    pi_1 = vars['pi_1']                 # Add on distance
    
    ## Vertical: Convert depths to heights
    # Define datum using MWL
    Y_datum = MWLR[0]

    # Convert heights to depths
    ZR = Y_datum - HR
    ZF = Y_datum - HF
    MWLR = MWLR - Y_datum

    ## Horizontal: Shifting and distance add-ons
    # Initial positions
    X_datum = XF[0]
    
    # Filtered: Align left
    XF = XF - X_datum
    WGF = WGF - X_datum
    XR = XR - X_datum
    WGR = WGR - X_datum

    # Define point to use
    XWKF = XF[WG_to_use]    # Position of wavemaker in x

    # Make a call to get_stability_vars (log beforehand)
    vars['h'] = ZF[0]   # Pass through an h to use
    output_vars = log_function_call(get_stability_vars)(vars)
    DX = output_vars['DX']
    L = output_vars['L_']

    # Add on Propagation Distance
    XF = np.insert(XF,0,-pi_1*L)
    ZF = np.insert(ZF,0,ZF[0])

    ## Shift coordinates to positive
    X_datum = XF[0]
    XF = XF  - X_datum
    WGF = WGF - X_datum
    XR = XR - X_datum
    WGR = WGR - X_datum

    # Get Xc_WK
    Xc_WK = WGF[WG_to_use]

    #%% Interpolation
    # Make sure unique (issue for some trials)
    unique_X, indices = np.unique(XF, return_index=True)
    sorted_indices = np.sort(indices)
    bathyX = XF[sorted_indices]
    # Interpolate to grid
    X_FW = np.arange(0, np.max(bathyX) + DX, DX)
    Z_FW = np.interp(X_FW, XF, ZF)

    #%% Variables to note
    # Positions of the actual wave gauges in the FUNWAVE outputs- what I need to compare
    adjusted_WG = WGR
    
    # Depth of the wavemaker
    DEP_WK = ZF[(np.abs(XF - XWKF)).argmin()]

    # Mglob
    Mglob = int(len(X_FW))

    # Prepare outputs (FUNWAVE)
    bathy_array = np.column_stack((X_FW, Z_FW))
    bathy_file = np.tile(Z_FW, (3, 1))

    # Prepare outputs (reference)
    raw_bathy = np.column_stack((XR, ZR))
    filt_bathy = np.column_stack((XF, ZF))

    # Update with new parameters
    # For FUNWAVE
    output_vars['bathy_array'] = bathy_array
    output_vars['bathy_file'] = bathy_file
    output_vars['Mglob'] = Mglob
    output_vars['DEP_WK'] = DEP_WK
    output_vars['Xc_WK'] = Xc_WK
    output_vars['WGF'] = WGF
    output_vars['WGR'] = WGR
    # For Reference
    output_vars['adjusted_WG'] = adjusted_WG
    output_vars['raw_bathy'] = raw_bathy
    output_vars['filt_bathy'] = filt_bathy
    #output_vars['MWL_adj'] = MWLR

    print('\t\tSucessfully processed bathymetry...')
    return output_vars