import pandas as pd
import pickle
import numpy as np

def get_spectra(vars):
    # Unpack Variables
    lo = vars['lo']
    hi = vars['hi']
    WG_to_use = vars['WG_to_use']
    pickle_file = vars['pickle_file']
    
    # Open pickled file
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
        f.close()
    
    ## Unpack variables from data
    t = data['filtered_data']['t']    
    t0 = data['filtered_data']['t0']  
    t_end = data['filtered_data']['t_end']     
    eta = data['filtered_data']['eta']    
    loc_x = data['filtered_data']['loc_x']
    
    # Select which wave gauge to use
    eta = np.squeeze(eta[:,WG_to_use])
    
    # Slice between start and end time, get to numpy
    teta = pd.DataFrame(t,index=t,columns=['time'])
    teta['eta'] = eta
    teta = teta.loc[t0:t_end]
    t = teta['time'].to_numpy()
    eta = teta['eta'].to_numpy()
    
    # Time step,length, and half length
    dt = t[1] - t[0]
    m = len(eta)
    M = (m+1)//2
    t_length = dt * m
    
    # Get the FFT
    fft_ = np.fft.fft(eta)
    
    # Fourier Coefficients
    a0 = np.real(fft_[0]) / m
    an = 2 * np.real(fft_[1:M]) / m
    bn = -2 * np.imag(fft_[1:M]) / m
    
    # Time/Indices in spectral space
    n = np.arange(len(an))
    x = np.arange(len(n)) * t_length / (len(n) - 1)
    
    # Amplitude and Phase
    cn = np.sqrt(an**2 + bn**2)
    en = np.arctan2(bn, an)
    
    # Apply cutoff frequencies
    mask = (np.arange(1, len(n) + 1) / t_length > lo) & (np.arange(1, len(n) + 1) / t_length < hi)
    filtered_n = np.where(mask)[0]
        
    per = t_length / (filtered_n + 1)
    cnn = cn[filtered_n]
    enn = en[filtered_n]
    
    # Get peak period and length
    NumWaveComp = len(per)
    PeakPeriod = np.max(per)
    
    # Output to dictionary
    spectra = {
        'per': per,
        'cnn': cnn,
        'enn': enn,
        'fourier': {
            'a0': a0,
            'an': an,
            'bn': bn
        },
        'loc_x': loc_x,
        'NumWaveComp': int(NumWaveComp),
        'PeakPeriod': PeakPeriod
    }
    
    return {'spectra': spectra,
            'PeakPeriod': PeakPeriod,
            'NumWaveComp': int(NumWaveComp)}