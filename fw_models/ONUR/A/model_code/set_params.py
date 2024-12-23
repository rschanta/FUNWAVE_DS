import funwave_ds.fw_py as fpy
import numpy as np
from scipy.optimize import fsolve
def set_params(vars):
    # Unpack Variables-------------------------------------------------
    Tperiod = vars['Tperiod']
    DEPTH_FLAT = vars['DEPTH_FLAT']
    SLP = vars['SLP']
    PI_1 = vars['PI_1']
    PI_2 = vars['PI_2']
    PI_3 = vars['PI_3']
    PI_4 = vars['PI_4']
    #-----------------------------------------------------------------

    # Estimate wavelength from linear dispersion
    # Find wavelength (L) through linear dispersion root-finding
    sigma = 2 * np.pi / Tperiod
    g = 9.81
    h = DEPTH_FLAT
    def disp_relation(k):
        return sigma**2 - g * k * np.tanh(k * h)
    
    k = fsolve(disp_relation, 0)[0]
    
    L = 2 * np.pi / k

    # Get DX from stability considerations
    DX = (L + 4*DEPTH_FLAT)/120
    DY = DX

    # Set the position of the wavemaker and sponge layer
    Xc_WK = PI_2*L
    Sponge_west_width = PI_3*L
    Xslp = (PI_2+PI_4)*L
    Mglob = int((Xslp + h/SLP)/(DX*(1-PI_1)))

    


    # Calculate Xslp and Mglob
    vars['Xslp'] = Xslp
    vars['Mglob'] = Mglob
    vars['DX'] = DX
    vars['DY'] = DY

    # Make a domain object and add bathymtery from it
    DOM = fpy.DomainObject2(var_dict = vars)
    DOM.z_from_dep_flat(vars)

    return {'DOM': DOM,
            'L': L,
            'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'Xslp': Xslp,
            'DEP_WK': DEPTH_FLAT}
