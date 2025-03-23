
def set_forcing(var_dict):
    
    # Unpack Variables-------------------------------------------------
    EPSILON = var_dict['EPSILON']
    DEPTH_FLAT = var_dict['DEPTH_FLAT']
    PI_3 = var_dict['PI_3']
    PI_4 = var_dict['PI_4']
    Tperiod = var_dict['Tperiod']
    TAU_1 = var_dict['TAU_1']
    #-----------------------------------------------------------------
    
    TOTAL_TIME = TAU_1*(PI_3+PI_4)*Tperiod
    
    AMP_WK = EPSILON*DEPTH_FLAT
    
    return {'TOTAL_TIME': TOTAL_TIME,
            'AMP_WK': AMP_WK}
    