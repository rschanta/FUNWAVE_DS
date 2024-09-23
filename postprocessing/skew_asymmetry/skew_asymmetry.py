import numpy as np
from scipy.signal import hilbert


def calculate_skewnewss(eta):
    # Subtract out mean
    eta_n = eta - np.mean(eta)
    
    # Calculate skewness 
    sk_num = np.mean(eta_n**3)
    sk_denom = (np.mean(eta_n**2))**(1.5); 
    skewness = sk_num/sk_denom
    
    return skewness

def calculate_asymmetry(eta):
    # Subtract out mean
    eta_n = eta - np.mean(eta)
    
    # Calculate asymmetry 
    hn = np.imag(hilbert(eta_n))
    hnn = hn - np.mean(hn)
    asy_num = np.mean(hnn ** 3)
    asy_denom = (np.mean(eta_n**2))**(1.5); 
    asymmetry = asy_num/asy_denom
    
    return asymmetry


def calculate_ska_1D(eta):
    '''
    Applies `calculate_skew` and `calculate_asymmetry` along the COLUMNS 
    of eta
    '''
    skewness = np.apply_along_axis(calculate_skewnewss, axis=0, arr=eta)
    asymmetry = np.apply_along_axis(calculate_asymmetry, axis=0, arr=eta)

    return skewness, asymmetry



