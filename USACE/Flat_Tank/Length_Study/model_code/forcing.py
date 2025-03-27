
def set_forcing(var_dict):
    
    # Unpack Variables-------------------------------------------------
    EPSILON = var_dict['EPSILON']
    DEPTH_FLAT = var_dict['DEPTH_FLAT']
    Tperiod = var_dict['Tperiod']
    TAU_1 = var_dict['TAU_1']
    #-----------------------------------------------------------------
    print('\t\tStarted Specification of Forcing...')

    # Set the total time condition- note tau is just factor of period here
    TOTAL_TIME = TAU_1*Tperiod
    
    # Set the amplitude of the wave
    AMP_WK = EPSILON*DEPTH_FLAT
    
    print('\t\tSuccessfully Set up Forcing!')
    return {'TOTAL_TIME': TOTAL_TIME,
            'AMP_WK': AMP_WK}
    