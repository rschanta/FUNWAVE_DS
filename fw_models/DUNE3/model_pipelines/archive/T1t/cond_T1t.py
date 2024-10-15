import os
import sys
import numpy as np

## FUNWAVE_DS Modules
import funwave_ds.fw_py as fpy
import funwave_ds.fw_tf as ftf
import funwave_ds.fw_fs as fwf

## model_code module
import model_code as mod    


# Get input dictionary
In_d_i = fpy.load_input_dict_i()

# Define internal postprocessing functions
function_set = [fwf.animate_1D_eta,
                fwf.animate_1D_undertow,
                fwf.animate_1D_roller]

# Define internal plot/print functions

# Load in data, post-process, and serialize
serialized_features = ftf.internal_postprocess(In_d_i,function_set)

# Save the tfrecord
ftf.save_tfrecord(serialized_features)


    