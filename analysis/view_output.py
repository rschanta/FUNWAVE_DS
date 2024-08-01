## Necessary Imports
import os 

import pathlib
import pickle
import sys
# Path Commands
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
import python_code as fp
import tensorflow as tf






## Get the input summary directory
In_d = fp.tf.load_In_d_windows('In_d.pkl')

## Specify trial number
tri_num = 78

## Specify tensor shapes
tensors_3d = ['eta','dep']
tensors_2d = ['bathy','time_dt']

## Any other keys to add?
others = {'TOTAL_TIME':tf.io.FixedLenFeature([], tf.int64),
          'foo':tf.io.FixedLenFeature([], tf.int64),}

## Any other keys to ignore/remove?
keys_to_ignore = ['foo']

## Path to tfrecord files
paths = ['out_00078.tfrecord','out_00079.tfrecord']

## Get the dictionary
results = fp.tf.get_tfrecord_as_dict(tensors_3d,tensors_2d,others,In_d,keys_to_ignore,tri_num,paths)


## View/animation
fp.py.animate_eta_1D(results['input_00078'],'animate',100,fr=50)