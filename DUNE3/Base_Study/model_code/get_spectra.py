import funwave_ds as fds
def get_spectra(var_dict):
    # Unpack -----------------------------------------------------------------
    D3_Trial = int(var_dict['D3_Trial'])
    t = var_dict['data'][f'tri_{D3_Trial:02}']['f_t']
    eta = var_dict['data'][f'tri_{D3_Trial:02}']['f_eta_i'][:,0]
    t0 = var_dict['data'][f'tri_{D3_Trial:02}']['f_t0'] 
    t_end = var_dict['data'][f'tri_{D3_Trial:02}']['f_t_end'] 
    T_lower = var_dict['T_lower']
    T_higher = var_dict['T_higher']
    # ------------------------------------------------------------------------
    
    # Filter out time
    t_mask = (t>=t0) & (t<=t_end)

    # Get t and eta in this timeframe
    t = t[t_mask]
    eta = eta[t_mask]

    
    # Do the Fourier Analysis
    f_lo = 1/T_higher
    f_hi = 1/T_lower
    f,amp,phase = fds.WK_TIME_SERIES.get_fft_values(t=t,eta=eta,f_lo=f_lo,f_hi=f_hi)

    # Make the wavemaker object
    WK = fds.WK_TIME_SERIES(period=1/f,amp=amp,phase=phase)
    
    return {'WK': WK, 
            'NumWaveComp': WK.NumWaveComp,
            'PeakPeriod': WK.PeakPeriod}
