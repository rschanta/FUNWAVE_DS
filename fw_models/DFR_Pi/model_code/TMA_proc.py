def get_period(vars):
    # Unpack vars needed
    FreqPeak = vars['FreqPeak']
    Tperiod = 1/FreqPeak

    return {'Tperiod': Tperiod}