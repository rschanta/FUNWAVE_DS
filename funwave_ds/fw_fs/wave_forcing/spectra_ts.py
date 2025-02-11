import numpy as np
import pandas as pd
def get_spectra_time_series(df_spectra_ts,lo,hi):
    t = df_spectra_ts['t'].values
    eta = df_spectra_ts['eta'].values
    
    dt = t[1]-t[0]     # time step
    N = len(eta)       # record length
    fft_values = np.fft.fft(eta) 
    freqs = np.fft.fftfreq(N, d=dt)
    
    # Cut to Nyquist
    freqs = freqs[:N//2]
    fft_values = fft_values[:N//2]
    
    # Amplitude and Phase at each frequency
    amp = 2*np.abs(fft_values) /N
    phase = -np.angle(fft_values)
    
    df_spectra = pd.DataFrame({'freq': freqs,
                               'amp': amp,
                               'pha': phase})
    
    df_spectra = df_spectra[(df_spectra['freq'] < hi) & (df_spectra['freq'] > lo)]
    
    df_spectra['per'] = 1/df_spectra['freq']

    return df_spectra