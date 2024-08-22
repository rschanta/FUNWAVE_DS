def get_period(vars):
    # Unpack vars needed
    WAVEMAKER = vars['WAVEMAKER']

    if WAVEMAKER == 'WK_TIME_SERIES':
        Tperiod = vars['PeakPeriod']
        return {'Tperiod': Tperiod}
    elif WAVEMAKER == 'WK_IRR':
        FreqPeak = vars['FreqPeak']
        Tperiod = 1/FreqPeak
        return {'Tperiod': Tperiod}
    elif WAVEMAKER == 'WK_REG':
        return

    