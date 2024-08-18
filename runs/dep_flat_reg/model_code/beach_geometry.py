import numpy as np
def beach_geometry_1(vars):
    L = vars['L_']  # Wavelength

    chi = vars['CHI_Xslp']  
    gamma = vars['GAMMA_BEACH']  
    sigma = vars['SIGMA_SP']  
    omega = vars['OMEGA_WK']

    DX = vars['DX']
    DEPTH_FLAT = vars['DEPTH_FLAT']
    SLP = vars['SLP']

    # Set Xslp at chi times Wavelength
    Xslp = chi*L
    # Calculate required Mglob for this
    Mglob = int((Xslp + DEPTH_FLAT/SLP)/(gamma*DX))

    # Set sponge and wavemaker relative to wavelength
    Sponge_west_width = sigma*L
    Xc_WK = omega*L

    return {'Xslp': Xslp,
            'Mglob': Mglob,
            'Sponge_west_width': Sponge_west_width,
            'Xc_WK': Xc_WK}


def bathy_for_dep_flat(vars):
    DEPTH_FLAT = vars['DEPTH_FLAT']
    Xslp = vars['Xslp']
    DX = vars['DX']
    SLP = vars['SLP']
    Mglob = vars['Mglob']

    # Initialize Bathy array
    z = [DEPTH_FLAT] * Mglob
    
    # Get indices of sloping portion
    indices = list(range(int(Xslp // DX), Mglob))
    
    # Add onto portion
    for i in indices:
        z[i] = DEPTH_FLAT - SLP * (i - Xslp // DX) * DX
    
    # Construct x axis
    x = [i * DX for i in range(Mglob)]
    
    # Bathy
    bathy = np.column_stack((x, z))
    # Construct output dictionary

    return {'bathy': bathy}