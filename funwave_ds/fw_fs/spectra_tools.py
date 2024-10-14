import numpy as np
import pandas as pd

def calculate_spectra(time_series,lo,hi):
    '''
    
    INPUTS
        - time_series (pandas DataFrame): column of 'time' and then 'eta'
        - lo (float): upper cutoff frequency (Hz)
        - hi (float): upper cutoff frequency (Hz)
    '''
    
    t = time_series['time'].to_numpy()
    eta = time_series['eta'].to_numpy()
    
    # Get sampling time and record length
    dt = t[1]-t[0]     # time step
    N = len(eta)       # record length
    
    # FFT and Frequency Axis
    fft_values = np.fft.fft(eta) 
    freqs = np.fft.fftfreq(N, d=dt)
    
    # Cut to Nyquist
    freqs = freqs[:N//2]
    fft_values = fft_values[:N//2]
    
    # Amplitude at each frequency
    amp = 2*np.abs(fft_values) /N
    phase = -np.angle(fft_values)
    
    # Make periods
    periods = 1 /freqs

    # Combine into DataFrame
    spectra = pd.DataFrame({ 
                            'freqs': freqs,
                            'period': periods,
                            'amplitude': amp,
                            'phase': phase
                            })
    
    # Filter to frequencies of interest
    spectra = spectra[spectra['freqs'].between(lo, hi)]
    
    return spectra