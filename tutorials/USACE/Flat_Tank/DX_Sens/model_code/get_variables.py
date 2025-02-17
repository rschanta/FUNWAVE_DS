import pandas as pd

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


