import tensorflow as tf

def _parse_function_skew(proto, feature_description):
    # Parse
    parsed_features = tf.io.parse_single_example(proto, feature_description)

    # Decode/reshape the serialized tensors
    bathyZ = parsed_features['bathyZ']
    bathyZ = tf.io.parse_tensor(bathyZ, out_type=tf.float32)
    bathyZ = tf.reshape(bathyZ, [100, 1])

    skew = parsed_features['skew']
    skew = tf.io.parse_tensor(skew, out_type=tf.float32)
    skew = tf.reshape(skew, [100, 1])

    # Get other inputs, reshape
    Hmo = parsed_features['Hmo']
    Hmo = tf.io.parse_tensor(Hmo, out_type=tf.float32)
    Hmo = tf.reshape(Hmo, [1,1])
    
    Tperiod = parsed_features['Tperiod']
    Tperiod = tf.io.parse_tensor(Tperiod, out_type=tf.float32)
    Tperiod = tf.reshape(Tperiod, [1,1])
    
    # Create tuple THIS NEEDS TO BE A TUPLE FOR CONSISTENT OUTPUTS
    inputs = (Hmo, bathyZ, Tperiod)
    outputs = skew
    
    return inputs, outputs


def _parse_function_asy(proto, feature_description):
    # Parse
    parsed_features = tf.io.parse_single_example(proto, feature_description)

    # Decode/reshape the serialized tensors
    bathyZ = parsed_features['bathyZ']
    bathyZ = tf.io.parse_tensor(bathyZ, out_type=tf.float32)
    bathyZ = tf.reshape(bathyZ, [100, 1])

    asy = parsed_features['asy']
    asy = tf.io.parse_tensor(asy, out_type=tf.float32)
    asy = tf.reshape(asy, [100, 1])

    # Get other inputs, reshape
    Hmo = parsed_features['Hmo']
    Hmo = tf.io.parse_tensor(Hmo, out_type=tf.float32)
    Hmo = tf.reshape(Hmo, [1,1])
    
    Tperiod = parsed_features['Tperiod']
    Tperiod = tf.io.parse_tensor(Tperiod, out_type=tf.float32)
    Tperiod = tf.reshape(Tperiod, [1,1])
    
    # Create tuple THIS NEEDS TO BE A TUPLE FOR CONSISTENT OUTPUTS
    inputs = (Hmo, bathyZ, Tperiod)
    outputs = asy
    
    return inputs, outputs

def parse_function_skew(tf_record_files,feature_description):
    dataset = tf.data.TFRecordDataset(tf_record_files)
    dataset = dataset.map(lambda proto: _parse_function_skew(proto,feature_description))
    return dataset

def parse_function_asy(tf_record_files,feature_description):
    dataset = tf.data.TFRecordDataset(tf_record_files)
    dataset = dataset.map(lambda proto: _parse_function_asy(proto,feature_description))
    return dataset


def _parse_function_dummy(proto, feature_description):
    # Parse
    parsed_features = tf.io.parse_single_example(proto, feature_description)

    # Decode/reshape the serialized tensors
    bathyZ = parsed_features['bathyZ']
    bathyZ = tf.io.parse_tensor(bathyZ, out_type=tf.float32)
    bathyZ = tf.reshape(bathyZ, [100, 1])

    skew = parsed_features['skew']
    skew = tf.io.parse_tensor(skew, out_type=tf.float32)
    skew = tf.reshape(skew, [100, 1])

    # Get other inputs, reshape
    Hmo = parsed_features['Hmo']
    Hmo = tf.io.parse_tensor(Hmo, out_type=tf.float32)
    Hmo = tf.reshape(Hmo, [1,1])
    
    Tperiod = parsed_features['Tperiod']
    Tperiod = tf.io.parse_tensor(Tperiod, out_type=tf.float32)
    Tperiod = tf.reshape(Tperiod, [1,1])
    
    # Dummy output
    dummy_output = tf.concat([skew, Hmo, Tperiod], axis=0) 
    print("Shape of dummy_output:", dummy_output.shape)
    # Create tuple THIS NEEDS TO BE A TUPLE FOR CONSISTENT OUTPUTS
    inputs = (Hmo, bathyZ, Tperiod)
    outputs = dummy_output
    
    return inputs, dummy_output

def parse_function_dummy2(tf_record_files,feature_description):
    dataset = tf.data.TFRecordDataset(tf_record_files)
    dataset = dataset.map(lambda proto: _parse_function_dummy(proto,feature_description))
    return dataset
