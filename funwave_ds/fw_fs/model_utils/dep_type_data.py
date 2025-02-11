from ..utils.check_params import check_required_params
from ..wave_forcing.dispersion import linear_dispersion_by_roots
from ..wave_forcing.get_rep_variables import get_rep_period
from ..utils.stability import get_DX_Torres
from ...fw_py.net_cdf import DomainObject3
import numpy as np

def interpolate_stable(X,Z,DX):
    # Make sure unique X
    unique_X, indices = np.unique(X, return_index=True)
    sorted_indices = np.sort(indices)
    bathyX = X[sorted_indices]

    # Interpolate to grid
    X_FW = np.arange(0, np.max(bathyX) + DX, DX)
    Z_FW = np.interp(X_FW, X, Z)

    return X_FW,Z_FW





def set_stable_1D_bathy_data(var_dict):
    '''
    Makes a stable 1D profile with the wavemaker on the leftmost point
    '''
    # Unpack Variables-------------------------------------------------
    PI_2 = var_dict['PI_2']
    PI_3 = var_dict['PI_3']
    PI_4 = var_dict['PI_4']
    df_bathy = var_dict['df_bathy']
    X = df_bathy['X'].values
    Z = df_bathy['Z'].values
    #-----------------------------------------------------------------

    # Get representative period
    Trep = get_rep_period(var_dict)

    # Let first point of Z be the representative depth
    h = Z[0]

    # Get wavelength and wave number
    k,L = linear_dispersion_by_roots(Trep,h)

    # Get DX from stability considerations
    DX = get_DX_Torres(L,h)

    # Define the add-on distance (left align plus pi params)
    add_dist = (PI_2 + PI_4)*L - X[0] 

    # Add-on the distance (need another point)
    X = np.insert(X + add_dist,0,0)
    Z = np.insert(Z,0,Z[0])

    # Interpolate to stable grid
    X,Z = interpolate_stable(X,Z,DX)
    
    # Position of Wavemaker based on Pi_2
    Xc_WK = PI_2*L
    DEP_WK = h
    # Position of Wavemaker based on Pi_3
    Sponge_west_width = PI_3*L

    # Mglob, Nglob
    Mglob = len(X)
    Nglob = 3
    DY = DX

    # Make Domain Object
    DOM = DomainObject3(DX = DX, DY = DX, 
                        Mglob = Mglob, Nglob = 3)
    # Add the data to it
    DOM.z_from_1D_array(Z)



    return {'DOM': DOM,
            'Mglob': Mglob,
            'Nglob': Nglob,
            'DX': DX,
            'DY': DY,
            'L': L,
            'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'DEP_WK': DEP_WK}