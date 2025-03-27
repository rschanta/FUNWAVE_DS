
# Module imports
import funwave_ds.fw_fs as ffs
import funwave_ds.fw_py as fpy

def get_bathy(var_dict):
    # Unpack -----------------------------------------------------------------
    Z = var_dict['Z']
    X = var_dict['X']
    PI_2 = var_dict['PI_2']
    PI_3 = var_dict['PI_3']
    PI_4 = var_dict['PI_4']
    L = var_dict['L']
    MWL_left = var_dict['MWL_left']
    # Unpack -----------------------------------------------------------------

    DX = L/70
    DY = L/70

    # Distance to add 
    dist_add = (PI_4+PI_2)*L
    Xa,Za = ffs.add_flat_distance(X,Z,dist_add,side='left')
    
    # Interpolate and align to grid
    X_FW,Z_FW = ffs.interpolate_align(Xa,Za,DX)
    Z_FW = MWL_left - Z_FW
    
    # Mglob, Nglob
    Mglob = len(X_FW)
    Nglob = 3
    
    # Wavemaker position
    Xc_WK = PI_2*L
    DEP_WK = MWL_left
    
    # Sponge position
    Sponge_west_width = PI_3*L
    
    # Make Domain Object
    DOM = fpy.DomainObject3(DX = DX, DY = DY, 
                        Mglob = Mglob, Nglob = 3)
    # Add the data to it
    DOM.z_from_1D_array(Z_FW)
    
    return {'DOM': DOM,
            'Mglob': Mglob,
            'Nglob': Nglob,
            'DX': DX,
            'DY': DY,
            'L': L,
            'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'DEP_WK': DEP_WK}
