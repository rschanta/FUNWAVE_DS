import pandas as pd
import pickle
import numpy as np

def get_pi_vars(vars):
    print('\tStarted applying variables dependent on pi parameters...')
    # Unpack Variables
    pi_1 = vars['pi_1']
    pi_2 = vars['pi_2']
    pi_3 = vars['pi_3']
    pi_4 = vars['pi_4']

    h = vars['DEPTH_FLAT']
    SLP = vars['SLP']

    L = vars['L_']
    DX = vars['DX']

    # Position of wavemaker
    Xc_WK = pi_2*L

    # Position of sponge
    Sponge_west_width = pi_3*L

    # Xslp required
    Xslp = (pi_2+pi_4)*L

    # Mglob required
    Mglob = int((Xslp + h/SLP)/(DX*(1-pi_1)))

    print('\tFinished applying variables dependent on pi parameters...')

    return {'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'Xslp': Xslp,
            'Mglob': Mglob}