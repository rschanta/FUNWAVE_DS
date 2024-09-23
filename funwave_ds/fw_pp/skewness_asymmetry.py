def calculate_skewness(eta):
     '''
    Calculates the skewness of a 1D time series in eta
    '''
    # Subtract out mean
    eta_n = eta - np.mean(eta)
    
    # Calculate skewness 
    sk_num = np.mean(eta_n**3)
    sk_denom = (np.mean(eta_n**2))**(1.5); 
    skewness = sk_num/sk_denom
    
    return skewness


def calculate_asymmetry(eta):
    '''
    Calculates the asymmetry of a 1D time series in eta
    '''
    # Subtract out mean
    eta_n = eta - np.mean(eta)
    
    # Calculate asymmetry 
    hn = np.imag(hilbert(eta_n))
    hnn = hn - np.mean(hn)
    asy_num = np.mean(hnn ** 3)
    asy_denom = (np.mean(eta_n**2))**(1.5); 
    asymmetry = asy_num/asy_denom
    
    return asymmetry


def ska_app_1D(eta):
    '''
    Applies `calculate_skew` and `calculate_asymmetry` along the COLUMNS 
    of eta, assuming eta is 2D and rows are time steps and columns are
    position in the cross-shore
    '''
    skewness = np.apply_along_axis(calculate_skewness, axis=0, arr=eta)
    asymmetry = np.apply_along_axis(calculate_asymmetry, axis=0, arr=eta)

    return skewness, asymmetry


def calculate_ska_1D(vars):
    '''
    Calculates the skew and asymmetry for every point in the domain 
    for a 1D FUNWAVE simulation, cutting the time series after the
    time specified in `STEADY_TIME`. It assumes that Nglob = 3
    '''
    # Unpack variables
    eta = vars['eta']
    mask = vars['mask']
    time = vars['time'][:,0]
    steady_time = vars['STEADY_TIME'][:,0]

    # Apply mask
    eta[mask == 0] = np.nan
    
    # Cut to steady time
    steady_i = np.searchsorted(time, STEADY_TIME)
    eta_cut = eta[steady_i:, :]

    # Apply ska_app_1d
    skewness,asymmetry = calculate_ska_1D(eta_cut)

    return {'skewness': skewness,
            'asymmetry': asymmetry}