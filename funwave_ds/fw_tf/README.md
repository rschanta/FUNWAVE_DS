# `fw_tf`: Tensorflow Utility
LAST UPDATED: 10/14/2024


The `fw_tf` submodule contains functions that wrap around TensorFlow functions to effectively compress FUNWAVE output in data-efficient ways and prepare it for machine-learning workflows. The tensorflow tensor is the primary object used to manipulate FUNWAVE outputs, but this data format is more broadly compatible with numpy as well.

The ultimate goal of compression in the tensorflow `tf.data` ecosystem is to store the data as *.tfrecord* files, which is an efficient way to serialize data. This process is somewhat complicated, and more documentation concerning this can be found HERE.

It is worth noting the default types used in tensorflow:
- Floats/doubles are always created as or cast to `float32`
- Integers are always created/cast as `int64`
- Booleans are consistently cast to strings, either `T` or `F`, as in FUNWAVE/FORTRAN

|File| Purpose|Functions within|
|:--|:--|:--|
|[feature_description_type](./feature_description_type.py) | Create feature descriptions for an Example protocol buffer, based on type| `get_feature_desc_tensors`, `get_feature_desc_strings`, `get_feature_desc_floats`, `get_feature_desc_ints`| 
|[feature_description](./feature_description.py) | Create a feature description dictionary to use in the serialization/parsing process for FUNWAVE parameters| `construct_feature_descr`, `get_feature_desc_inputs`, `add_features_manually` | 
|[parsing_deserialization](./parsing_deserialization.py) | Read data from a serialized formats of the `tf.data` ecosystem to humanly readable formats | `deserialize_tensor`, `_parse_function`, `parse_function`, `parse_spec_var`, `parse_to_dataset`| 
|[save_tf_record](./save_tf_record.py) | Save a given serialized dictionary to a `.tfrecord` file| `save_tf_record`, `plot_TS_spectra`| 
|[get_io](./get_io.py) | Get FUNWAVE inputs/outputs| `get_inputs`, `get_outputs`| 
|[serialization_type](./serialization_pp.py) | Serialize data in an appropriate manner for their type| `serialize_tensor`,`serialize_int`, `serialize_float`, `serialize_string`| 
|[serialization](./serialization.py) | Serializes dictionaries of data| `serialize_dictionary`,`internal_postprocess`| 
|[tensor_stacking](./tensor_stacking.py) | Functions used to stack the raw outputs of FUNWAVE (ie- eta_XXXXX.txt) into tensorflow tensors| `load_array`,`get_MNglob`, `load_and_stack_to_tensors`| 