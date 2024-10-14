'''
get_rep_period
    - Gets represenative period to use for stability calculations
'''

def get_period(vars):
    print('\t\tStarted finding a representative period...')
    # Unpack vars needed
    WAVEMAKER = vars['WAVEMAKER']

    if WAVEMAKER == 'WK_TIME_SERIES':
        Tperiod = vars['PeakPeriod']
        print('\t\t\t Using PeakPeriod for time-series spectra wave.')
        print('\t\tSuccessfully found a representative period!')
        return {'Tperiod': Tperiod}
    
    return

    