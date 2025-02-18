import numpy as np

def set_stations(var_dict):
    # Unpack Variables-------------------------------------------------
    DOM = var_dict['DOM']


    Xc_WK = var_dict['Xc_WK']
    L = var_dict['L']

    DX = var_dict['DX'] 

    PI_1 = var_dict['PI_1']  
    PI_2 = var_dict['PI_2']  
    PI_3 = var_dict['PI_3'] 

    #-----------------------------------------------------------------
    print('\t\tStarted setting upstations...')

    start_Xpos_sta = Xc_WK+ L
    start_Mglob_sta = int((start_Xpos_sta)/DX)

    # End gages at edge of propagation distance (assuming 50 wavelengths)
    end_Xpos_sta = start_Xpos_sta + PI_3*L
    end_Mglob_sta = int((end_Xpos_sta)/DX)

    # Linspace 50 points and round
    stations_M = np.linspace(start_Mglob_sta, end_Mglob_sta, 50)
    stations_M = np.round(stations_M).astype(int)


    print(f'\t\t Number of Stations Created: {len(stations_M)}')

    # Assert that there are 50 stations
    assert len(stations_M) == 50, "Not 50 stations for each!"

    # Make Nglob
    stations_N = np.ones(50)

    # Update the domain object
    DOM.add_stations(Mglob_pos=stations_M,
                    Nglob_pos=stations_N)

    # Return
    print('\t\tSuccessfully set up stations!')
    return {'DOM': DOM}