import numpy as np

def set_stations(var_dict):
    # Unpack Variables-------------------------------------------------
    DOM = var_dict['DOM']


    Xc_WK = var_dict['Xc_WK']
    l = var_dict['l']

    DX = var_dict['DX'] 

    PI_1 = var_dict['PI_1']  
    PI_2 = var_dict['PI_2']  
    PI_3 = var_dict['PI_3'] 

    #-----------------------------------------------------------------
    print('\t\tStarted setting upstations...')

    start_Xpos_sta = Xc_WK+ l
    start_Mglob_sta = int((start_Xpos_sta)/DX)

    # End gages at edge of propagation distance (assuming 50 wavelengths)
    end_Xpos_sta = (PI_1 + PI_2 + PI_3)*l
    end_Mglob_sta = int((end_Xpos_sta)/DX)
    # End gages at edge of propagation distance (assuming 49 wavelengths)
    end_Xpos_sta_49 = (PI_1 + PI_2 + PI_3+ 1)*l
    end_Mglob_sta_49 = int((end_Xpos_sta_49)/DX)

    # Spacing in terms of Mglob
    gage_spacing_Mglob = int(l/DX)



    # Space out stations evently
    stations_M = np.arange(start_Mglob_sta, 
                        end_Mglob_sta, 
                        gage_spacing_Mglob)

    # Fix if less than 50 (could be 49)
    if len(stations_M)<50:
        stations_M = np.arange(start_Mglob_sta, 
                            end_Mglob_sta_49,   # Only difference is this line
                            gage_spacing_Mglob)



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