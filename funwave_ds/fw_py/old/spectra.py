import numpy as np
from scipy.fft import fft


""" def get_TS_spectra(t, eta, lo, hi):

    Arguments:
    - t: (n x 1 numpy array) time series
    - eta: (n x 1 numpy array) eta series
    - lo: (float) cutoff frequency on the low end
    - hi: (float) cutoff frequency on the high end

    Returns:
    - spectra: (dict) dictionary with the following fields:
        - per: (n x 1 array) array of periods for wavemaker
        - cnn: (n x 1 array) array of amplitudes for each period, unscaled
        - enn: (n x 1 array) array of phase shifts
        - fourier: (dict) contains Fourier coefficients directly
            - a0: (float) first term
            - an: (n x 1 array) cosine terms
            - bn: (n x 1 array) sine terms
        - peak_per: (float) period associated with the highest amplitude (cnn)
        - num_components: (int) number of components (length of cnn array)

    # Get time series and eta series
    t = t - np.min(t)  
    dt = t[1] - t[0]  

    # Length of series and first half
    m = len(eta)
    M = (m + 1) // 2

    # FFT and Processing
    d = fft(eta)
    t_length = dt * m  # Length of time record

    # Fourier Coefficients
    a0 = d[0] / m  # First term
    an = 2 * np.real(d[1:M]) / m  # Cosine coefficients
    bn = -2 * np.imag(d[1:M]) / m  # Sine coefficients

    # Time/Indices in spectral space
    n = np.arange(1, len(an) + 1)
    x = np.arange(len(n)) * t_length / (len(n) - 1)

    # Amplitude and Phase
    cn = np.sqrt(an**2 + bn**2)
    en = np.arctan2(bn, an)

    # Apply cutoff frequencies
    per = []
    cnn = []
    enn = []
    for j in range(len(n)):
        ff = (j + 1) / t_length  # frequency of j-th harmonic
        if lo < ff < hi:
            per.append(t_length / (j + 1))
            cnn.append(cn[j])
            enn.append(en[j])

    per = np.array(per)
    cnn = np.array(cnn)
    enn = np.array(enn)

    # Find the peak period
    peak_per = per[np.argmax(cnn)] if len(cnn) > 0 else None

    # Number of components
    num_components = len(cnn)

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
        'peak_per': peak_per,
        'num_components': num_components
    }

    return spectra
 """