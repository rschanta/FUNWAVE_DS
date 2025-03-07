

def set_FW_params(var_dict):
    ## UNPACK ----------------------------------------------------------------
    # Stability add-on
    PI_1 = var_dict['PI_1']
    PI_2 = var_dict['PI_2']
    h_offshore = var_dict['h_offshore']
    L = var_dict['L']
    XI_1 = var_dict['XI_1']
    TAU_1 = var_dict['TAU_1']
    Tperiod = var_dict['Tperiod']
    ## [END] UNPACK ----------------------------------------------------------
    print('\t\tStarting setting FUNWAVE parameters...')
    
    
    Xc_WK = (PI_1 + PI_2)*L
    Sponge_west_width =PI_1*L
    DEP_WK = h_offshore
    AMP_WK = XI_1*h_offshore
    TOTAL_TIME = TAU_1*Tperiod
    
    print('\t\tSuccessfully set FUNWAVE parameters!')
    return {'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'DEP_WK': DEP_WK,
            'AMP_WK': AMP_WK,
            'TOTAL_TIME': TOTAL_TIME}