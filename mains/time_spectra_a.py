import sys
import os

## Custom Modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../model_runs')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../packages')))
import time_spectra_a_f as ts


def main(super_path, run_name):
    super_path = './local_lustre'
    run_name = 'TSPY'
    trial_path = 'Trial05.pkl'
    ts.generate_in(super_path,run_name,trial_path)


#%% Test out




