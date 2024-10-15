#%% Load modules
import os
import numpy as np
import tensorflow as tf
import sys

import funwave_ds.fw_py as fpy
import funwave_ds.fw_tf as ftf
sys.path.append("/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi")
sys.path.append("/work/thsu/rschanta/RTS-PY/")
import model_code as mod
import ml_models as ml

## Get paths
p = fpy.get_FW_paths()
ptr = fpy.get_FW_tri_paths()
tri_num = int(os.getenv('TRI_NUM'))
paths = [f'/work/thsu/rschanta/DATA/DFR_Pi/TMA3/fw_outputs/Out_{tri_num:05}.tfrecord']

## Parse in features to dictionary
parsed_dict = ftf.parse_spec_var(paths,
            tensors_3D = ['eta'],
            tensors_2D = ['bathy','time_dt'],
            floats = ['DX','Xc_WK','Hmo','Tperiod'],
            strings = [])

## Apply post-processed features
out_dict =  ml.ska_conv_1.preprocessing_pipeline4(parsed_dict[f'tri_{tri_num:05}'],0)

## Serialize the post-processed features
feature_dict_ML = ftf.serialize_dictionary(out_dict,{})

## Save out 
ftf.save_tfrecord2(feature_dict_ML,f'/work/thsu/rschanta/DATA/DFR_Pi/TMA3/ML_inputs/MLin_{tri_num:05}.tfrecord')

