'''
get_pickles
    - Get the paths to the pickled data of Dune 3 Runs 5-24
        and pull out the bathymetry and MWL from the files
'''

import os
import pickle
def get_pickle_data(vars):
    print('\t\tStarted finding pickled data...')

    # Unpack Variables
    D3_trial = vars['D3_trial']
    DATA_DIR = vars['DATA_DIR']


    # Construct path to pickle
    pickle_file = os.path.join(DATA_DIR, 'Dune3/Inputs/pickles', f'Trial{int(D3_trial):02}.pkl')

    # Get data from the pickled file
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
        f.close()

    D3_raw = data['raw_data']
    raw_bathy = D3_raw['bed_before']
    XR = raw_bathy[:,0]         # X position as given
    HR = raw_bathy[:,1]         # height as given
    WGR = D3_raw['WG_loc_x']    # Wave gauge position
    MWLR = D3_raw['MWL']        # MWL height at wave gauge position

    # Filtered Data
    D3_fil = data['filtered_data']
    filt_bathy = D3_fil['bed_num_before']
    XF = filt_bathy[:,0]        # X position as given
    HF = filt_bathy[:,1]        # height as given
    WGF = D3_fil['loc_x']       # position where spectra were calculated
    
    

    print(f'\t\tSuccessfully found pickled data from: {pickle_file}')
    return {'pickle_file': pickle_file,
            'XR': XR,
            'HR': HR,
            'WGR': WGR,
            'MWLR': MWLR,
            'XF': XF,
            'HF': HF,
            'WGF': WGF}



