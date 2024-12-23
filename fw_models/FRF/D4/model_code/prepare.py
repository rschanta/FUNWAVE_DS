import dask.dataframe as dd
import numpy as np
from scipy.optimize import fsolve
import pandas as pd
import funwave_ds.fw_py as fpy
def set_params(vars):
    # Unpack Variables-------------------------------------------------
    PI_2 = vars['PI_2']
    PI_3 = vars['PI_3']
    dataset = vars['dataset']
    profile_list = vars['profile_list']
    prof_num = vars['prof_num']
    #-----------------------------------------------------------------

    ## Read in the data
    ddf = dd.read_parquet(dataset)
    MLS = pd.read_csv(profile_list).to_numpy().flatten()

    #%% Unpack the variables
    grab_profile = ddf[ddf['MLID']==MLS[int(prof_num)]]
    unpackvars = ['waveHs','waveTp', 'day','year','month','MLID','surveyNumber','profileNumber','FID']
    v_ = {}
    for var in unpackvars:
        v_[var] = grab_profile[var].unique().values.compute()[0]

    #%% Compute
    grab_profile = grab_profile.compute()

    #%% Extract out info
    dest = grab_profile.sort_values(by='xFRF')
    H = -dest['elevation'].iloc[-1]
    x = dest['xFRF'].to_numpy()
    z = -dest['elevation'].to_numpy()

    ## Dispersion ------------------------------------------
    sigma = 2 * np.pi / np.float64(v_['waveTp'])

    def disp_relation(k):
        return sigma**2 - 9.81 * k * np.tanh(k * H)

    k = fsolve(disp_relation, 0)[0]
    L = 2 * np.pi / k
    kh = k*H
    DX = (L + 4*H)/120
    ## Dispersion ------------------------------------------


    ## Add propagation distance ----------------------------
    x = dest['xFRF'].to_numpy()
    x_new = np.append(x,x[-1] + PI_2*L)
    z_new = np.append(z,z[-1])
    ## Add propagation distance ----------------------------

    ## Set Params ------------------------------------------
    Xc_WK = PI_2*L
    Sponge_west_width = PI_3*L
    Hmo = np.float64(v_['waveHs'])
    Tperiod = np.float64(v_['waveTp'])
    FreqPeak = 1/Tperiod
    DEP_WK = np.float64(H)
    ## Set Params ------------------------------------------

    ## Sort  -----------------------------------------------
    unique_X, indices = np.unique(x_new, return_index=True)
    sorted_indices = np.sort(indices)
    bathyX = x_new[sorted_indices]
    ## Sort  -----------------------------------------------


    ## Interpolate to Grid /Flip --------------------------
    X_FW = np.arange(x_new[0], np.max(bathyX) + DX, DX)
    Z_FW = np.interp(X_FW, x_new, z_new)
    Z_FW = np.flip(Z_FW)
    vars['DEP_WK']= DEP_WK
    vars['DX'] = DX
    vars['DY'] = DX
    vars['Mglob'] = int(len(X_FW))
    vars['Nglob'] = int(3)
    ## Interpolate to Grid  --------------------------------


    # Make Domain Object -----------------------------------
    DOM = fpy.DomainObject2(var_dict = vars)
    DOM.z_from_1D_array(Z_FW)
    # Make Domain Object -----------------------------------

    print('\t\tSucessfully processed bathymetry...')
    #-----------------------------------------------------------------
    return {'DOM': DOM,
            'DEP_WK': DEP_WK,
            'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'Hmo': Hmo,
            'Tperiod': Tperiod,
            'FreqPeak': FreqPeak,
            'L_': L}
    #-----------------------------------------------------------------