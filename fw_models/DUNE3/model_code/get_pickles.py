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
    
    print(f'\t\tSuccessfully found pickled data from: {pickle_file}')
    return {'pickle_file': pickle_file,
            'bathyX': bathyX,
            'bathyh': bathyh,
            'MWL': MWL}