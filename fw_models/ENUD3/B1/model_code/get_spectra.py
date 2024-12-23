import pandas as pd
import numpy as np
import funwave_ds.fw_fs as fws
import funwave_ds.fw_py as fpy
import xarray as xr
def set_WAVEMAKER(vars):
    print('\t\tStarted setting wavemaker...')

    #----------------------------------------------------------------- 
    # Unpack xarray objects
    D3Object = vars['D3Object']
    t = D3Object.coords['T_DATA'].values
    eta = D3Object['etaD3'].values

    # Unpack other variables
    lo = vars['lo']
    hi = vars['hi']
    #-----------------------------------------------------------------

    ## Calculate spectra to return object
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
    
    # Combine into dataframe
    df_spectra = pd.DataFrame({ 
                        'freqs': freqs,
                        'period': 1 /freqs,
                        'amplitude': amp,
                        'phase': phase
                        })
    

    # Cut to between low and high frequencies 
    df_spectra_cut = df_spectra[df_spectra['freqs'].between(lo, hi)]
    
    
    # Add spectra along a coordinate
    perr = df_spectra_cut['period'].to_numpy()
    ampp = df_spectra_cut['amplitude'].to_numpy()


    WK_Object = xr.Dataset(
        # Variables
        {
            'amp2': (['period'], df_spectra_cut['amplitude']),
            'phase2': (['period'], df_spectra_cut['phase']),
        },
        
        # Coordinates
        coords={
            # Raw coordinates
            'period': (['period'], df_spectra_cut['period']),
        },
        
        # Attributes
        attrs={
            'PeakPeriod': perr[np.argmax(ampp)],
            'NumWaveComp': len(perr)
        }
        )   

    
    return {'WKK': WK_Object,
            'NumWaveComp': len(perr),
            'PeakPeriod': perr[np.argmax(ampp)]}