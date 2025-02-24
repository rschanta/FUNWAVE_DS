import funwave_ds.fw_fs as ffs


def get_hydro(var_dict):
    # UNPACK FROM LOADED DATA ------------------
    Z = var_dict['Z']
    MWL_left = var_dict['MWL_left']
    period = var_dict['PeakPeriod']

    print('\t\tStarted getting hydrodynamic variables from dispersion...')

    # Get water depth
    h = MWL_left - Z[0]


    k,L = ffs.linear_dispersion_by_roots(period,h)
    kh = k*h

    print('\t\tFinished getting hydrodynamic variables from dispersion!')
    return {'k': k,
            'L': L,
            'kh': kh}


