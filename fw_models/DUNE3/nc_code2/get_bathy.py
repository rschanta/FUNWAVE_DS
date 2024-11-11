import numpy as np
from .get_stability import get_stability_vars
from funwave_ds.fw_py.record import log_function_call
import funwave_ds.fw_py as fpy
import xarray as xr

## Interpolate Bathymetry correctly
def interpolate_bathy(XF,ZF,DX):
        ## Ensure points in X are uniqe
        unique_X, indices = np.unique(XF, return_index=True)    # Unique X value indices
        sorted_indices = np.sort(indices)                       # These indices sorted
        bathyX = XF[sorted_indices]                             # Pre-interpolation X values    

        ## Interpolate to grid
        X_FW = np.arange(0, np.max(bathyX) + DX, DX)            # FUNWAVE X Points
        Z_FW = np.interp(X_FW, XF, ZF)                          # FUNWAVE Z Points

        return X_FW, Z_FW

'''
get_bathy_new()
    - second version of applying the bathymetry, used for D3e
'''

def get_bathy(vars):
    print('\t\tStarted processing bathymetry...')

    #-----------------------------------------------------------------
    # Unpack xarray objects
    D3Object = vars['D3Object']   
    # Coordinates
    XR = D3Object.coords['D3r_X'].values                # Raw X positions
    XF = D3Object.coords['D3f_X'].values                # Filtered X positions
    WGR = D3Object.coords['D3r_loc_x'].values           # Raw position of the wave gauges in X
    WGF = D3Object.coords['D3f_loc_x'].values           # Filtered position of the wave gauges in X
    # Variables
    HR = D3Object['D3r_Z'].values          # Raw bathymetry heights from bottom of flume
    HF = D3Object['D3f_Z'].values          # Filtered bathymetry heights from bottom of flume
    MWLR = D3Object['D3r_MWL'].values      # Raw MWL at wave gauges
    
    # Unpack Variables 
    WG_to_use = vars['WG_to_use']           # spectra position to use
    pi_1 = vars['pi_1']                     # Add on distance
    #-----------------------------------------------------------------

    ## VERTICAL Processing
    ver_shift = MWLR[0]                # Horizontal shift value
    vars_to_vshift = [HR, HF, MWLR]    # Variables to shift vertically    
    v_shifted_vars = [ver_shift - var for var in vars_to_vshift]               
    ZR, ZF, MWLR = v_shifted_vars 

    ## STABILITY: Calculate wavelenth and DX
    vars['h'] = ZF[0]   # Pass through an h to use
    output_vars = log_function_call(get_stability_vars)(vars)
    DX = output_vars['DX']
    L = output_vars['L_']

    ## HORIZONTAL Processing
    hor_shift = pi_1*L -   XF[0]                                   # Horizontal shift value      
    vars_to_hshift = [XF, WGF, XR, WGR]                            # Variables to shift horizontally
    h_shifted_vars = [var + hor_shift for var in vars_to_hshift]  
    XF, WGF, XR, WGR = h_shifted_vars

    ## Add on western points
    XF = np.insert(XF,0,0)
    ZF = np.insert(ZF,0,ZF[0])
    
    ## Interpolation
    X_FW, Z_FW = interpolate_bathy(XF,ZF,DX)
    
    ## FUNWAVE variables needed
    Xc_WK = WGF[WG_to_use]
    DEP_WK = ZF[(np.abs(XF - 0)).argmin()]
    vars['DX'] = DX
    vars['DY'] = DX
    vars['Mglob'] = int(len(X_FW))
    vars['Nglob'] = int(3)

    # Make the Domain Object, and height to it
    DOM = fpy.DomainObject2(var_dict = vars)
    DOM.z_from_1D_array(Z_FW)

    print('\t\tSucessfully processed bathymetry...')
    #-----------------------------------------------------------------
    return {'DOM': DOM,
            'DEP_WK': DEP_WK,
            'Xc_WK': Xc_WK,
            'L_': L}
    #-----------------------------------------------------------------