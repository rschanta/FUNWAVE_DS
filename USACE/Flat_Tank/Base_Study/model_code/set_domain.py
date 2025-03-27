
import numpy as np

import funwave_ds as fpy

def set_spatial_domain(var_dict):
    # Unpack Variables-------------------------------------------------
    # Hydrodynamics
    L = var_dict['L']
    # Domain
    DEPTH_FLAT = var_dict['DEPTH_FLAT']
    # Nondimensional Parameters
    PI_1 = var_dict['PI_1']  
    PI_2 = var_dict['PI_2']  
    PI_3 = var_dict['PI_3'] 
    PI_4 = var_dict['PI_4'] 
    PI_5 = var_dict['PI_5']
    #-----------------------------------------------------------------
    print('\t\tStarted setting up domain...')

    # DX: Use L/70
    DX = L/70

    # Set sponge widths
    Sponge_west_width = PI_1*L
    Sponge_east_width = PI_5*L

    # Set wavemaker position, depth, and amplitude
    Xc_WK = (PI_1+PI_2)*L
    DEP_WK = DEPTH_FLAT
    
    # Calculate total domain size
    width = (PI_1+PI_2+PI_3+PI_4+PI_5)*L
    Mglob = int(width//DX) + 1
    
    # Construct the domain
    DOM = fpy.DomainObject3(DX = DX,
                            DY = DX,
                            Mglob = Mglob,
                            Nglob = 3)
    
    # Add bathymetry to the domain
    DOM.z_from_FLAT(DEPTH_FLAT)

    # Return new parameters
    print('\t\tSuccessfully set up domain!')
    return {'Sponge_west_width': Sponge_west_width,
            'Sponge_east_width': Sponge_east_width,
            'Xc_WK': Xc_WK,
            'DEP_WK': DEP_WK,
            'Mglob': int(Mglob),
            'DOM': DOM,
            'DX': DX,
            'DY': DX
            }
    
    
