import pandas as pd
import numpy as np
# The linear dispersion relation
def f(k,w,h,g):
    return g*k*np.tanh(k*h) - w**2 

# Derivative of linear dispersion relationship with respect to k
def dfdk(k,w,h,g):
    return g*(np.tanh(k*h) + h*k*np.cosh(k*h)**-2)

# Newton-Raphson Method for Root-Finding
def ldis(T,h,k=1,g=9.81):
    # Newton-Raphson Method: Convergence criteria & max iterations
    errorTolerance = 10**-12
    maxIterations = 20
    
    # Calculate angular frequency
    w = 2*np.pi/T
    
    # Loop through until max iterations or convergence criteria met
    for i in range(maxIterations):
        
        # Newton's Method Equations
        correction = -f(k,w,h,g)/dfdk(k,w,h,g)
        k += correction
        
        # Check convergence: how small is correction?
        error = correction/k
        if ( abs(error) < errorTolerance):
            break
        
        # Calculate wavelength    
        l = 2*np.pi/k
        
    return l

## WAVE CELERITY CALCULATOR
def wavespeed(T,L):
    c = L / T
    return c


def get_hydro(var_dict):
    # Unpack Variables-------------------------------------------------
    Tperiod = var_dict['Tperiod']
    DEPTH_FLAT = var_dict['DEPTH_FLAT']
    #-----------------------------------------------------------------
    print('\t\tStarted calculating hydrodynamics...')

    # Calculate wavelength and celeity
    L = ldis(Tperiod,DEPTH_FLAT,k=1,g=9.81)
    c = wavespeed(Tperiod,L)

    # Rounded wavelength
    l = int(np.round(L))

    # Return
    print('\t\tSuccessfully calculated hydrodynamic variables!')
    return {'L': L,
            'c': c,
            'l': l
            }

