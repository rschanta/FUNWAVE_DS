#%% Load modules
import os
import numpy as np
import tensorflow as tf
import sys

import funwave_ds.fw_py as fpy
import funwave_ds.fw_tf as ftf
import funwave_ds.fw_ml as fml
sys.path.append("/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi")
sys.path.append("/work/thsu/rschanta/RTS-PY")
import ml_models.ska_conv_1 as ml

#%% Get files
directory = "/work/thsu/rschanta/DATA/DFR_Pi/TMA2/ML_inputs"
files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


#%% Parse Data
tensors_2D = ['bathyZ','skew','asy','Hmo','Tperiod']
feature_description = ftf.construct_feature_descr(tensors_2D = tensors_2D, strings = [])


# Split file paths into train/test/validation sets
train_set, val_set = fml.split_paths(0.8,files)
    
# Parse both sets
train_set = ml.parse_function_skew(train_set,feature_description)
val_set = ml.parse_function_skew(val_set,feature_description)

# Shuffle the set
train_set = train_set.shuffle(buffer_size=500)
val_set = val_set.shuffle(buffer_size=500)
    
# Batching 
train_set = train_set.batch(32)
val_set = val_set.batch(32)
    
# Prebatch
train_set = train_set.prefetch(buffer_size=tf.data.AUTOTUNE)
val_set = val_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    
# Create the model
model = ml.create_model_skew2()
model.compile(optimizer='adam', loss='mse')
model.summary()

# Fit the model
history = model.fit(train_set, epochs = 100,validation_data=val_set)

import matplotlib.pyplot as plt

# Plot the training loss
plt.plot(history.history['loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.show()
plt.savefig('/work/thsu/rschanta/DATA/DFR_Pi/TMA2/models/training_loss_plot_skew.png')
# Save the model in HDF5 format
model.save('/work/thsu/rschanta/DATA/DFR_Pi/TMA2/models/model_skew2.h5')

# Save the model in Keras format
model.save('/work/thsu/rschanta/DATA/DFR_Pi/TMA2/models/model_skew2.keras', save_format='keras')