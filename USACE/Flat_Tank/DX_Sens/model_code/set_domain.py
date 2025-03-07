import funwave_ds.fw_py as fpy

def calculate_DX(h,l,PI_6):
    # Stability limits from Torres et al
    h_lim = h/15
    l_lim = l/60

    min_lim = min(h_lim, l_lim)
    max_lim = max(h_lim, l_lim)
    valid_range = max_lim - min_lim

    DX = min_lim + PI_6*valid_range

    return DX


def set_domain(var_dict):
    # Unpack Variables-------------------------------------------------
    # Hydrodynamics
    L = var_dict['L']
    Tperiod = var_dict['Tperiod']
    # Domain
    DEPTH_FLAT = var_dict['DEPTH_FLAT']
    # Nondimensional Parameters
    PI_1 = var_dict['PI_1']  
    PI_2 = var_dict['PI_2']  
    PI_3 = var_dict['PI_3'] 
    PI_4 = var_dict['PI_4'] 
    PI_5 = var_dict['PI_5']
    PI_6 = var_dict['PI_6']  
    TAU_1 = var_dict['TAU_1']
    XI_1 = var_dict['XI_1']

    #-----------------------------------------------------------------
    print('\t\tStarted setting domain/forcing...')

    # Calculate DX
    DX = calculate_DX(DEPTH_FLAT,L,PI_6)

    # Set sponge widths
    Sponge_west_width = PI_1*L
    Sponge_east_width = PI_5*L

    # Set wavemaker position, depth, and amplitude
    Xc_WK = (PI_1+PI_2)*L
    DEP_WK = DEPTH_FLAT
    AMP_WK = XI_1*DEPTH_FLAT

    # Calculate total domain size
    width = (PI_1+PI_2+PI_3+PI_4+PI_5)*L
    Mglob = int(width//DX) + 1

    # Calculate total time
    TOTAL_TIME = TAU_1*Tperiod

    # Make a domain object and construct
    DOM = fpy.DomainObject3(DX = DX,
                            DY = DX,
                            Mglob = Mglob,
                            Nglob = 3)
    DOM.z_from_2D_array(DEPTH_FLAT)


    # Return
    print('\t\tSuccessfully set up domain!')
    return {'Sponge_west_width': float(Sponge_west_width),
            'Sponge_east_width': float(Sponge_east_width),
            'Xc_WK': float(Xc_WK),
            'DEP_WK': float(DEP_WK),
            'AMP_WK': float(AMP_WK),
            'Mglob': int(Mglob),
            'TOTAL_TIME': float(TOTAL_TIME),
            'DOM': DOM,
            'DX': DX,
            'DY': DX
            }
