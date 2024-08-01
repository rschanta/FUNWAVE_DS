import numpy as np
from scipy.signal import hilbert


def calculate_ska_1D(eta):
    '''
    Calculates the skew and asymmetry for a 2D array where each row corresponds
    to a different time step, and each column a different place in space, 
    intended for a 1D simulation
    '''
    eta_n = eta - np.mean(eta)
    denom = (np.mean(eta_n**2))**(1.5); 
    # Numerator for skew
    sk_num = np.mean(eta_n**3)
    # Numerator for Asymmetry
    hn = np.imag(hilbert(eta_n))
    hnn = hn - np.mean(hn)
    asy_num = np.mean(hnn ** 3)
    # Calculate and output
    skew = sk_num/denom;
    asy = asy_num/denom;
    return skew, asy



