import argparse
import os 
import sys
import tensorflow as tf
import pickle

import funwave_ds.fw_py as fpy
import funwave_ds.fw_tf as ftf
sys.path.append("/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi")
sys.path.append("/work/thsu/rschanta/RTS-PY/")
import model_code as mod
import ml_models as ml

# Directory where all the inputs are store
directory = '/work/thsu/rschanta/DATA/DFR_Pi/TMA3/ML_inputs'

# Get all files in the directory
files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

paths = sorted(files)

## Parse in features to dictionary
tensors_2D = ['bathyX','bathyZ','skew','Hmo','Tperiod','asy']
parsed_dict = ftf.parse_spec_var(paths,
            tensors_2D = tensors_2D,
            strings = [])


## Save out
with open('/work/thsu/rschanta/DATA/DFR_Pi/TMA3/ML_comp/postprocessed.pkl', 'wb') as f:
    pickle.dump(parsed_dict, f)

