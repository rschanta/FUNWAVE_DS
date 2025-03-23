import numpy as np
def set_friction(var_dict):
    # Unpack Variables-------------------------------------------------
    # Hydrodynamics
    L = var_dict['L']
    # Friction
    Cd = var_dict['Cd_regional']
    # Nondimensional Parameters
    PI_1 = var_dict['PI_1']
    PI_2 = var_dict['PI_2']
    PI_6 = var_dict['PI_6']
    PI_7 = var_dict['PI_7']
    # Domain
    DOM = var_dict['DOM']
    #-----------------------------------------------------------------
    X = DOM['X'].values
    
    
    # Find x levels
    x_fric_lo = (PI_1+PI_2+PI_7-PI_6/2)*L
    x_fric_hi = (PI_1+PI_2+PI_7+PI_6/2)*L
    
    # Find index
    i_fric_lo = np.argmin(np.abs(X-x_fric_lo))
    i_fric_hi = np.argmin(np.abs(X-x_fric_hi))

    friction_array = np.zeros(DOM.attrs['Mglob'])
    friction_array[i_fric_lo:i_fric_hi+1] = Cd
    

    DOM.friction_from_1D_array(friction_array)
    
    return {'DOM': DOM}
    