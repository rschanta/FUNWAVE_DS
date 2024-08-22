def get_TMA(vars):
    print('\tStarted processing TMA data...')
    
    # Unpack Variables (note choice of bathy set by stability)
    PeakPeriod = vars['PeakPeriod']
    Hmo = vars['Hmo']

    # Get as frequency
    FreqPeak = 1/PeakPeriod
    
    print('\tSuccessfully processed TMA data!\n')

    return {'FreqPeak': FreqPeak}