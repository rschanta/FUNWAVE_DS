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


#%%



## Get the input summary directory
In_d = fp.tf.load_In_d_windows('In_d.pkl')

## Specify trial number
tri_num = 3

## Specify tensor shapes
tensors_2d = ['AMP_WK','Tperiod', 'bathyZ','skew','asy']
feature_descriptions = fp.tf.get_feature_desc_tensors(tensors_2d, 2,{})

## Path to tfrecord files
paths = ['MLin_00003.tfrecord']

## Get the dictionary
dataset = fp.tf.parse_function(paths,feature_descriptions,tensors_2d)
for record in dataset:
    feature_keys = list(record.keys())
    print(f'Feature keys: {feature_keys}')
#%%
for idx, parsed_features in enumerate(dataset):
    parsed_dict = {}
    for key, value in parsed_features.items():
        parsed_dict[key] = value.numpy()


#%% ML section
tensors_2d = ['bathyZ','skew','asy','AMP_WK','Tperiod'] 
feature_description = fp.tf.get_feature_desc_tensors(tensors_2d, 2,{})
    
#%% Define the parsing
tf_record_files_train = ['MLin_00001.tfrecord']
tf_record_files_val=['MLin_00003.tfrecord']

training_set = fp.ml.ska_conv.parse_function_dummy2(tf_record_files_train,feature_description)
val_set = fp.ml.ska_conv.parse_function_dummy2(tf_record_files_val,feature_description)
#%% Create and fit the model
model = fp.ml.ska_conv.create_model_dummy2()
model.compile(optimizer='adam', loss='mse')
model.summary()
training_set = training_set.batch(1)
val_set = val_set.batch(1)
model.fit(training_set, validation_data=val_set)

lister = [parsed_dict['AMP_WK'], parsed_dict['bathyZ'], parsed_dict['Tperiod']]
z = model.predict(lister)