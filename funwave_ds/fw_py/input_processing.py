import numpy as np
def bathy_from_dep_flat(Mglob, FWS):
    D = FWS['DEPTH_FLAT']
    Xslp = FWS['Xslp']
    DX = FWS['DX']
    SLP = FWS['SLP']
    # Initialize Bathy array
    z = [D] * Mglob
    
    # Get indices of sloping portion
    indices = list(range(int(Xslp // DX), Mglob))
    
    # Add onto portion
    for i in indices:
        z[i] = D - SLP * (i - Xslp // DX) * DX
    
    # Construct x axis
    x = [i * DX for i in range(Mglob)]
    
    # Construct output dictionary
    bathy = {
        'bathy_file': [z, z, z],
        'array': np.column_stack((x, z))
    }
    
    return bathy