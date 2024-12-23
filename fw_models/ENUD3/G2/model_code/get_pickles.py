'''
get_pickles
    - Get the paths to the pickled data of Dune 3 Runs 5-24
        and pull out the bathymetry and MWL from the files
'''

import os
import xarray as xr
import funwave_ds.fw_py as fpy
import pickle

def get_pickle_data(vars):
    print('\t\tStarted finding pickled data...')
    
    #-----------------------------------------------------------------
    # Unpack Variables
    D3_trial = vars['D3_trial']
    DATA_DIR = vars['DATA_DIR']
    #-----------------------------------------------------------------
    
    
    pickle_file = os.path.join(DATA_DIR, 'Dune3/Inputs/pickles', f'Trial{int(D3_trial):02}.pkl')

    # Get data from the pickled file
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
        f.close()


    ## Get into an xarray
    D3Object = xr.Dataset(
    # Variables
    {
        # Raw variables
        'D3r_MWL': (['D3r_loc_x'], data['raw_data']['MWL']),
        'D3r_Z': (['D3r_X'], data['raw_data']['bed_before'][:, 1]),
        'ETA_DATA': (['T_DATA','GAGE_DATA_X'], data['raw_data']['eta']),

        # Filtered variables
        'D3f_Z': (['D3f_X'], data['filtered_data']['bed_num_before'][:, 1]),
        'etaD3': (['T_DATA'], data['filtered_data']['eta_i'][:, 0])
    },
    # Coordinates
    coords={
        # Raw coordinates (used for comparisons)
        'D3r_X': (['D3r_X'], data['raw_data']['bed_before'][:, 0]),
        'GAGE_DATA_X': (['GAGE_DATA_X'], data['raw_data']['WG_loc_x']),
        'T_DATA': (['T_DATA'], data['filtered_data']['t']),
        
        # Filtered coordinates (used for actual inputs)
        'D3f_X': (['D3f_X'], data['filtered_data']['bed_num_before'][:, 0]),
        'D3f_loc_x': (['D3f_loc_x'], data['filtered_data']['loc_x'])
    },
    # Attributes
    attrs={
        'D3_TRIAL': data['raw_data']['trial_name']
    }
)


    print(f'\t\tSuccessfully found pickled data from: {pickle_file}')


    return {'pickle_file': pickle_file,
            'D3Object': D3Object}



