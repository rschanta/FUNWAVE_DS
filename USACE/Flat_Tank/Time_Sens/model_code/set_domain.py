import funwave_ds.fw_py as fpy

def set_domain(var_dict):
    # Unpack Variables-------------------------------------------------
    DX = var_dict['DX']
    DEPTH_FLAT = var_dict['DEPTH_FLAT']

    l = var_dict['l']
    c = var_dict['c']

    PI_1 = var_dict['PI_1']  
    PI_2 = var_dict['PI_2']  
    PI_3 = var_dict['PI_3'] 
    PI_4 = var_dict['PI_4'] 
    PI_5 = var_dict['PI_5']   
    TAU_1 = var_dict['TAU_1']
    XI_1 = var_dict['XI_1']
    
    Nglob = var_dict['Nglob']

    #-----------------------------------------------------------------
    print('\t\tStarted setting domain/forcing...')

    # Set sponge widths
    Sponge_west_width = PI_1*l
    Sponge_east_width = PI_5*l

    # Set wavemaker position, depth, and amplitude
    Xc_WK = (PI_1+PI_2)*l
    DEP_WK = DEPTH_FLAT
    AMP_WK = XI_1*DEPTH_FLAT

    # Calculate total domain size
    width = (PI_1+PI_2+PI_3+PI_4+PI_5)*l
    Mglob = int(width//DX) + 1

    # Calculate total time
    TOTAL_TIME = TAU_1*l/c

    # Make a domain object and construct
    DOM = fpy.DomainObject3(DX = DX,
                            DY = DX,
                            Mglob = Mglob,
                            Nglob = Nglob)
    DOM.z_flat(DEPTH_FLAT)


    # Return
    print('\t\tSuccessfully set up domain!')
    return {'Sponge_west_width': float(Sponge_west_width),
            'Sponge_east_width': float(Sponge_east_width),
            'Xc_WK': float(Xc_WK),
            'DEP_WK': float(DEP_WK),
            'AMP_WK': float(AMP_WK),
            'Mglob': int(Mglob),
            'TOTAL_TIME': float(TOTAL_TIME),
            'DOM': DOM
            }
