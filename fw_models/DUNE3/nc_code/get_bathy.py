import numpy as np
from .get_stability import get_stability_vars
from funwave_ds.fw_py.record import log_function_call
import funwave_ds.fw_py as fpy


'''
get_bathy_new()
    - second version of applying the bathymetry, used for D3e
'''
def get_bathy(vars):
    print('\t\tStarted processing bathymetry...')
    
    # Unpack Variables 
    D3Object = vars['D3Object']                
    pi_1 = vars['pi_1']
    bathyX = D3Object.coords.D3f_X
    bathyh = D3Object.vars.D3f_Z.value
    MWL = D3Object.vars.D3r_MWL.value


    # Subtract mean of the MWL
    datum = np.nanmean(MWL)
    bathyZ = datum - bathyh

    # Get height needed for stability calcs (just left-most height)
    h = bathyZ[0]
    vars['DEPTH_FLAT'] = h

    # Make a call to get_stability_vars (log beforehand)
    output_vars = log_function_call(get_stability_vars)(vars)
    
    DX = output_vars['DX']
    L = output_vars['L_']
    vars['DX'] = DX
    vars['DY'] = DX
    vars['L_'] = L
    # Calculate the amount to add, if needed, and add on
    X_add = pi_1*L 
    bathyX = bathyX + X_add

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
    bathy_file = np.tile(Z_out, (3, 1))


    # Set Mglob and Nglob
    vars['Mglob'] = int(len(X_out))
    vars['Nglob'] = int(3)

    # Make the Domain Object, and height to it
    DOM = fpy.DomainObject(vars)
    DOM.z_from_array(bathy_file.T)

    print('\t\tSucessfully processed bathymetry...')
    return {'DOM': DOM}