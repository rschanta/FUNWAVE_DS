'''
Tools to deal with the 'WK_TIME_SERIES' wavemaker from some given time series
'''
from ..wave_forcing import get_spectra_time_series


def set_WK_TIME_SERIES(var_dict):
    
    # Unpack Variables-------------------------------------------------
    FreqMin = var_dict['FreqMin']
    FreqMax = var_dict['FreqMax']
    df_spectra_ts = var_dict['df_spectra_ts']
    #-----------------------------------------------------------------
    
    # Get the spectra
    df_spectra = get_spectra_time_series(df_spectra_ts,FreqMin,FreqMax)

    # Get the Peak Period
    freq_peak = df_spectra['freq'].iloc[df_spectra['amp'].idxmax()]
    PeakPeriod = 1/freq_peak
    NumWaveComp = len(df_spectra)

    return {'PeakPeriod': PeakPeriod,
            'NumWaveComp': NumWaveComp,
            'df_spectra': df_spectra}



