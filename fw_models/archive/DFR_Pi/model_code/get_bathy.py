import numpy as np

def add_bathy(vars):

    print('\tStarted reconstructing bathymetry from geometry...')
    
    # Unpack Variables
    DX = vars['DX']
    h = vars['DEPTH_FLAT']
    SLP = vars['SLP']
    Xslp = vars['Xslp']
    Mglob = vars['Mglob']

    # Array
    z = [h] * Mglob
    
    # Get indices of sloping portion
    indices = list(range(int(Xslp // DX), Mglob))
    
    # Add onto portion
    for i in indices:
        z[i] = h - SLP * (i - Xslp // DX) * DX
    
    # Construct x axis
    x = [i * DX for i in range(Mglob)]
    
    # Construct output dictionary
    bathy = {
        'array': np.column_stack((x, z))
    }
    print('\tFinished reconstructing bathymetry from geometry...')
    return {'bathy': bathy}