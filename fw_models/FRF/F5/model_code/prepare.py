import dask.dataframe as dd
import numpy as np
from scipy.optimize import fsolve
import pandas as pd
import funwave_ds.fw_py as fpy
def set_params(vars):

    # Unpack Variables-------------------------------------------------
    PI_1 = vars['PI_1']
    PI_2 = vars['PI_2']
    PI_3 = vars['PI_3']

    Tperiod = vars['Tperiod']
    dataset = vars['dataset']
    prof_num = vars['prof_num']
    #-----------------------------------------------------------------

    ## Read in the data
    df = dd.read_parquet(dataset, filters=[('uniqueID', '==', prof_num)])
    df = df.compute()
    date = df['date'].iloc[0]
    year = df['year'].iloc[0]
    month = df['month'].iloc[0]
    day = df['day'].iloc[0]

    # Align to 0
    df['xFRF'] = df['xFRF'] - df['xFRF'].min()

    # Mirror the Data
    mirrored_X = 2 * df['xFRF'].iloc[-1] - df['xFRF'][::-1]
    mirrored_Y = df['elevation'][::-1]
    df = pd.DataFrame({'xFRF': mirrored_X, 'elevation': mirrored_Y})

    # Cutoff data if needed
    df = df[df['elevation']>-8]
    df['xFRF'] = df['xFRF'] - df['xFRF'].min()

    ## Add distance -------------------------------------
    # Offshore height
    H = -df['elevation'].iloc[0]                        

    # Get Wavelength from linear dispersion
    sigma = 2 * np.pi / np.float64(Tperiod)
    def disp_relation(k):
        return sigma**2 - 9.81 * k * np.tanh(k * H)
    k = fsolve(disp_relation, 0)[0]
    L = 2 * np.pi / k

    # Calculate distance to add
    dist_to_add = (PI_2 + PI_3)*L

    new_row = {'xFRF': -dist_to_add, 'elevation': -H}
    df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
    ## [END] Add distance -------------------------------------


    # Calculate DX Stability
    pos_H = np.abs(df['elevation'].iloc[0])
    kh = k*pos_H
    DX = (L + 4*pos_H)/120

    # Interpolate to Grid
    X_FW = np.arange(df['xFRF'].iloc[0], df['xFRF'].iloc[-1] + DX, DX)
    Z_FW = -np.interp(X_FW, df['xFRF'], df['elevation'])

    # Align once more
    X_FW = X_FW - np.min(X_FW)

    ## Set Params ------------------------------------------
    Xc_WK = PI_2*L
    Sponge_west_width = PI_1*L
    DEP_WK = np.float64(pos_H)


    vars['DEP_WK']= DEP_WK
    vars['DX'] = DX
    vars['DY'] = DX
    vars['Mglob'] = int(len(X_FW))
    vars['Nglob'] = int(3)


    # Make Domain Object -----------------------------------
    DOM = fpy.DomainObject2(var_dict = vars)
    DOM.z_from_1D_array(Z_FW)

    print('\t\tSucessfully processed bathymetry...')
    #-----------------------------------------------------------------
    return {'DOM': DOM,
            'DEP_WK': DEP_WK,
            'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'L_': L,
            'kh': kh,
            'date': date,
            'year': year,
            'month': month,
            'day': day}
    #-----------------------------------------------------------------