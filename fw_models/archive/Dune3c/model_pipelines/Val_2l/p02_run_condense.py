import sys
import numpy as np
# Add to system path
sys.path.append("/work/thsu/rschanta/RTS-PY")
# Get modules
import funwave_ds.fw_py as fpy
import funwave_ds.fw_tf as ftf

# Get input dictionary
In_d_i = fpy.load_input_dict()

# Compress/Serialize the outputs
serialized_features = ftf.serialize_outputs(In_d_i)

# Compress/Serialize the inputs
serialized_features = ftf.serialize_inputs(In_d_i,
                                           feature_dict = serialized_features)

# Compress/Serialize supplemental variables
supplemental_vars = {'bathy': In_d_i['bathy']['array'].astype(np.float32),
                     'spectra': In_d_i['spectra_array'].astype(np.float32)}
serialized_features = ftf.serialize_dictionary(supplemental_vars,feature_dict = serialized_features)

ftf.save_tfrecord2(serialized_features)

print('\nSuccessfully saved out compress tfrecord file!')



    