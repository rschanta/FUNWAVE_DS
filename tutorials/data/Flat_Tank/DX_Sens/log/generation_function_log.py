# Function: get_input_vars
# Code:
def get_input_vars(var_dict):
    # Unpack Variables-------------------------------------------------
    DATA_PATH = var_dict['DATA_PATH']
    SIM_NUMBER = var_dict['SIM_NUMBER']
    #-----------------------------------------------------------------
    print('\t\tStarted accessing input variables...')

    # Load in Parquet and index out sim number row
    df = pd.read_parquet(DATA_PATH)
    df = df[df['SIM_NUMBER']==SIM_NUMBER]
    
    # Get variables of interest
    Tperiod = float(df['Tperiod'].values[0])
    DEPTH_FLAT = float(df['DEPTH_FLAT'].values[0])
    DX = df['DX'].values[0]

    print(f"Tperiod {Tperiod}")
    print(f"DEPTH_FLAT {DEPTH_FLAT}")
    print(f"DX {DX}")
    # Return
    print('\t\tSuccessfully got input variables!')
    return {'Tperiod': Tperiod,
            'DEPTH_FLAT': DEPTH_FLAT,
            'DX': DX
            }

#----------------------------------------
# Function: get_hydro
# Code:
def get_hydro(var_dict):
    # Unpack Variables-------------------------------------------------
    Tperiod = var_dict['Tperiod']
    DEPTH_FLAT = var_dict['DEPTH_FLAT']
    #-----------------------------------------------------------------
    print('\t\tStarted calculating hydrodynamics...')

    # Calculate wavelength and celeity
    L = ldis(Tperiod,DEPTH_FLAT,k=1,g=9.81)
    c = wavespeed(Tperiod,L)

    # Rounded wavelength
    l = int(np.round(L))

    # Return
    print('\t\tSuccessfully calculated hydrodynamic variables!')
    return {'L': L,
            'c': c,
            'l': l
            }

#----------------------------------------
# Function: set_domain
# Code:
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

#----------------------------------------
# Function: set_stations
# Code:
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

#----------------------------------------
