'''
Functions to get representative hydrodynamic variables from the inputs, including
    > period
'''


def get_rep_period(ds):
    '''
    Gets a 'representative period' based on the type of wavemaker
    and calls it `Trep`, unifying the notation of the different wavemakers
    '''

    # Get wavemaker and get different types
    WAVEMAKER = ds['WAVEMAKER']

    # Regular Wavemaker
    if WAVEMAKER == 'WK_REG':
        Trep = ds['Tperiod']

    # Irregular, JONSWAP, and TMA
    elif WAVEMAKER in {'WK_IRR','JON_1D','JON_2D','TMA_1D'}:
        Trep = 1/ds['FreqPeak']

    # Time series
    elif WAVEMAKER in {'WK_TIME_SERIES'}:
        Trep = ds['PeakPeriod']

    # Raise error if not otherwise specified
    else:
        if "Tperiod" not in ds:
            raise KeyError("Not a standard wavemaker and no representative period `Trep` found!")


    return Trep



