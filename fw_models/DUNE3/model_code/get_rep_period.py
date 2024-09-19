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
    elif WAVEMAKER == 'WK_IRR':
        FreqPeak = vars['FreqPeak']
        Tperiod = 1/FreqPeak
        print('\t\t\t Using 1/FreqPeak for irregular wave.')
        print('\t\tSuccessfully found a representative period!')
        return {'Tperiod': Tperiod}
    elif WAVEMAKER == 'WK_REG':
        print('\t\t\t Using TPeriod in input file')
        print('\t\tSuccessfully found a representative period!')
        return

    