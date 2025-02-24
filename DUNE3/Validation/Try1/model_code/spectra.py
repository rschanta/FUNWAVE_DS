import numpy as np
import xarray as xr


def fft_analysis(t,eta):
    # Assert time and series the same length
    assert(len(t)==len(eta)),'t and eta must have the same length!'
    
    # Basic Info
    dt = t[1]-t[0]     # time step
    N = len(eta)       # record length
    
    # FFT and associated frequencies
    fft_values = np.fft.fft(eta) 
    f = np.fft.fftfreq(N, d=dt)

    # Cut to Nyquist
    f = f[:N//2]
    fft_values = fft_values[:N//2]

    # Amplitude and Phase at each frequency
    amp = 2*np.abs(fft_values) /N
    phase = -np.angle(fft_values)
    
    return f,amp,phase


def get_spectra(var_dict):
    print('\t\tStarted getting time series for spectra data...')


    # UNPACK FROM LOADED DATA ------------------
    # Get time
    tri_no = int(var_dict['D3_trial'])
    t_orig = var_dict[f'tri_{tri_no:02}']['f_t']
    t0 = var_dict[f'tri_{tri_no:02}']['f_t0']
    t_end = var_dict['tri_05']['f_t_end']
    
    # Get eta
    eta = var_dict[f'tri_{tri_no:02}']['f_eta_i']
    # UNPACK FROM LOADED DATA ------------------
    
    # Cut to just relevant times
    indices = (t_orig > t0) & (t_orig<t_end)
    t = t_orig[indices]
    eta = eta[indices,0]
    
    # Do Fourier Analysis
    f,amp,phase = fft_analysis(t,eta)
    
    # Convert to Period
    T = 1/f
    
    # PeakPeriod
    Tmax = T[np.argmax(amp)]
    
    
    ## MAKE AN OBJECT
    WK_Object = xr.Dataset(
        # Variables
        {
            'amp': (['period'], amp),
            'phase': (['period'], phase),
        },
        
        # Coordinates
        coords={
            # Raw coordinates
            'period': (['period'], T),
        },
        
        # Attributes
        attrs={
            'PeakPeriod': Tmax,
            'NumWaveComp': len(T)
        }
        )   
    print(Tmax)
    print('\t\tSuccessfully made spectra from time series!')
    return {'WK_Object': WK_Object,
            'NumWaveComp': len(T),
            'PeakPeriod': Tmax}

def set_spectra(var_dict):
    print('\t\tStarted cutting spectra to specified frequencies...')


    # UNPACK FROM LOADED DATA ------------------
    WK_Object = var_dict['WK_Object']
    period = WK_Object['period'].values
    amp = WK_Object['amp'].values
    phase = WK_Object['phase'].values

    # Cut off to lower and upper period bounds
    lo = var_dict['lo']
    hi = var_dict['hi']
    

    # Cut to just relevant times
    indices = (period > lo) & (period < hi)
    period = period[indices]
    phase = phase[indices]
    amp = amp[indices]

    
    # PeakPeriod
    PeakPeriod = period[np.argmax(amp)]
    print(PeakPeriod)
    # NumWaveComp
    NumWaveComp = len(period)
    
    
    ## MAKE AN OBJECT
    WK_Object = xr.Dataset(
        # Variables
        {
            'amp': (['period'], amp),
            'phase': (['period'], phase),
        },
        
        # Coordinates
        coords={
            # Raw coordinates
            'period': (['period'], period),
        },
        
        # Attributes
        attrs={
            'PeakPeriod': PeakPeriod,
            'NumWaveComp': NumWaveComp
        }
        )   
    print('\t\tSuccessfully cut to specified frequencies!')
    return {'WK_Object': WK_Object,
            'NumWaveComp': NumWaveComp,
            'PeakPeriod': PeakPeriod}