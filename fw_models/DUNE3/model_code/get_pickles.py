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

    # Bathymetry and MWL data
    bathy = data['filtered_data']['bed_num_before']
    MWL = data['raw_data']['MWL']
    bathyX = bathy[:,0]
    bathyh = bathy[:,1]
    
    # ADD 10_1_2024
    AMP_WK = data['raw_data']['Hmo'][0]/2
    Hmo = data['raw_data']['Hmo'][0]

    print(f'\t\tSuccessfully found pickled data from: {pickle_file}')
    return {'pickle_file': pickle_file,
            'bathyX': bathyX,
            'bathyh': bathyh,
            'MWL': MWL,
            'AMP_WK': AMP_WK,
            'Hmo': Hmo,
            'WG_loc_x': data['filtered_data']['loc_x']}



def get_pickle_raw_data(vars):
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

    # Bathymetry and MWL data
    bathy = data['raw_data']['bed_before']
    MWL = data['raw_data']['MWL']
    WG_loc_x = data['raw_data']['WG_loc_x']
    bathyX = bathy[:,0]
    bathyh = bathy[:,1]
    
    print(f'\t\tSuccessfully found pickled data from: {pickle_file}')
    return {'pickle_file': pickle_file,
            'bathyX': bathyX,
            'bathyh': bathyh,
            'MWL': MWL,
            'WG_loc_x': WG_loc_x}