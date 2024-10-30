'''
get_pickles
    - Get the paths to the pickled data of Dune 3 Runs 5-24
        and pull out the bathymetry and MWL from the files
'''

import os
import pickle
import funwave_ds.fw_py as fpy
def get_pickle_data(vars):
    print('\t\tStarted finding pickled data...')

    # Unpack Variables
    D3_trial = vars['D3_trial']
    DATA_DIR = vars['DATA_DIR']

    pickle_file = os.path.join(DATA_DIR, 'Dune3/Inputs/pickles', f'Trial{int(D3_trial):02}.pkl')

    # Get data from the pickled file
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
        f.close()

    D3Object = fpy.CoordinateObject()
    
    # Coordinates Variables
    D3Object.coords.D3f_X = data['filtered_data']['bed_num_before'][:,0]
    D3Object.coords.D3f_loc_x = data['filtered_data']['loc_x']
    D3Object.coords.D3r_loc_x = data['raw_data']['WG_loc_x']
    D3Object.coords.per = data['filtered_data']['wave_property'][:,1]


    # Variables
    D3Object.vars.D3f_Z = fpy.CoordVar(['D3f_X'],data['filtered_data']['bed_num_before'][:,1])
    D3Object.vars.D3r_MWL = fpy.CoordVar(['D3r_loc_x'],data['raw_data']['MWL'])
    D3Object.vars.amplitude = fpy.CoordVar(['per'],data['filtered_data']['wave_property'][:,0])
    D3Object.vars.phase = fpy.CoordVar(['period'],data['filtered_data']['wave_property'][:,0])


    ## Attributes
    D3Object.attrs.D3_TRIAL = data['raw_data']['trial_name']


    print(f'\t\tSuccessfully found pickled data from: {pickle_file}')


    return {'pickle_file': pickle_file,
            'D3Object': D3Object}



