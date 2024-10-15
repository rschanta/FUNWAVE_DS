import pickle
import os

def get_pickle_path(vars):
    print('\tStarted searching for pickled data...')
    # Unpack Variables
    D3_trial = vars['D3_trial']
    DATA_DIR = vars['DATA_DIR']
    # Construct path to pickle
    pickle_file = os.path.join(DATA_DIR, 'Dune3/Inputs/pickles', f'Trial{int(D3_trial):02}.pkl')
    print('\tSuccessfully found pickled data!\n')
    return {'pickle_file': pickle_file}