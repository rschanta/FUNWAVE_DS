from ..utils.check_params import check_required_params
from ..wave_forcing.dispersion import linear_dispersion_by_roots
from ..wave_forcing.get_rep_variables import get_rep_period
from ..utils.stability import get_DX_Torres
from ...fw_py.net_cdf import DomainObject3

def set_dep_type_slp(var_dict):
    '''
    Basic Tool to set up a dep_type_slp run based on best practices
    '''


    print('\tStarted setting parameters for DEPTH_TYPE=SLP...')

    # Check required parameters
    check_required_params(var_dict,['PI_1','PI_2','PI_3','PI_4', 'SLP','DEPTH_FLAT'])

    # Unpack Variables-------------------------------------------------
    DEPTH_FLAT = var_dict['DEPTH_FLAT']
    SLP = var_dict['SLP']
    PI_1 = var_dict['PI_1']
    PI_2 = var_dict['PI_2']
    PI_3 = var_dict['PI_3']
    PI_4 = var_dict['PI_4']
    #-----------------------------------------------------------------

    # Get representative period
    Trep = get_rep_period(var_dict)

    # Let DEPTH_FLAT be representative depth
    h = DEPTH_FLAT

    # Get wavelength and wave number
    k,L = linear_dispersion_by_roots(Trep,h)

    # Get DX from stability considerations
    DX = get_DX_Torres(L,h)

    # Position of Wavemaker based on Pi_2
    Xc_WK = PI_2*L
    # Position of Wavemaker based on Pi_3
    Sponge_west_width = PI_3*L
    # Xslp from PI_2 + PI_4
    Xslp = (PI_2+PI_4)*L
    
    # Mglob from geometric constraint
    Mglob = int((Xslp + h/SLP)/(DX*(1-PI_1)))

    # Let DEP_WK equal h
    DEP_WK = h
    # Set Nglob & DY
    Nglob = 3
    DY = DX

    # Make a domain object
    DOM = DomainObject3(DX = DX, DY = DY, 
                        Mglob = Mglob, Nglob = Nglob)
    # Add the DEPTH_TYPE=SLP depths to it
    DOM.z_from_dep_flat(DEPTH_FLAT=DEPTH_FLAT,
                        SLP=SLP, Xslp=Xslp)

    # Return variables added
    return {'DOM': DOM,
            'Mglob': Mglob,
            'Nglob': Nglob,
            'DX': DX,
            'DY': DY,
            'L': L,
            'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'Xslp': Xslp,
            'DEP_WK': DEP_WK}
