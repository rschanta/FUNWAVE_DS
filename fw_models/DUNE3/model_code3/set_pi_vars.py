'''
get_pi_vars
    - Set pi variables
'''

import pandas as pd
import numpy as np

def set_pi_vars(vars):
    print('\t\tStarted applying variables dependent on pi parameters...')
    # Unpack Variables
    pi_2 = vars['pi_2']
    L = vars['L_']

    # Position of sponge
    Sponge_west_width = pi_2*L

    print('\t\tFinished applying variables dependent on pi parameters...')

    return {'Sponge_west_width': Sponge_west_width}