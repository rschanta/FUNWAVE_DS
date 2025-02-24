
# Module imports
import funwave_ds.fw_fs as ffs
import funwave_ds.fw_py as fpy


def get_bathy(var_dict):
    print('\t\tStarted getting bathymetry and MWL...')

    # UNPACK FROM LOADED DATA ------------------
    tri_no = int(var_dict['D3_trial'])
    X = var_dict[f'tri_{tri_no:02}']['f_X_before']
    Z = var_dict[f'tri_{tri_no:02}']['f_bed_before']
    MWL_left = var_dict[f'tri_{tri_no:02}']['r_MWL'][0]

    print('\t\tFinished getting bathymetry and MWL!')
    return {'X': X,
            'Z': Z,
            'MWL_left': MWL_left}


def set_bathy(var_dict):
    print('\t\tStarted setting bathymetry via Pi parameters...')

    # UNPACK FROM LOADED DATA ------------------
    Z = var_dict['Z']
    X = var_dict['X']
    PI_2 = var_dict['PI_2']
    PI_3 = var_dict['PI_3']
    PI_4 = var_dict['PI_4']
    L = var_dict['L']
    h = Z[0]
    MWL = var_dict['MWL_left']
    # UNPACK FROM LOADED DATA ------------------

    # Get Stable DX/DY
    DX = ffs.get_DX_Torres(L,h)
    DY = DX

    # Distance to add 
    dist_add = (PI_4+PI_2)*L
    Xa,Za = ffs.add_flat_distance(X,Z,dist_add,side='left')

    # Interpolate and align to grid
    X_FW,Z_FW = ffs.interpolate_align(Xa,Za,DX)
    Z_FW = MWL - Z_FW

    # Mglob, Nglob
    Mglob = len(X_FW)
    Nglob = 3

    # Wavemaker position
    Xc_WK = PI_2*L
    DEP_WK = h

    # Sponge position
    Sponge_west_width = PI_3*L

    # Make Domain Object
    DOM = fpy.DomainObject3(DX = DX, DY = DX, 
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