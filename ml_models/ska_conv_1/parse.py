import tensorflow as tf

def _parse_function(proto, feature_description):
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
    AMP_WK = parsed_features['AMP_WK']
    AMP_WK = tf.io.parse_tensor(AMP_WK, out_type=tf.float32)
    AMP_WK = tf.reshape(AMP_WK, [1,1])
    
    Tperiod = parsed_features['Tperiod']
    Tperiod = tf.io.parse_tensor(Tperiod, out_type=tf.float32)
    Tperiod = tf.reshape(Tperiod, [1,1])
    
    # Create tuple THIS NEEDS TO BE A TUPLE FOR CONSISTENT OUTPUTS
    inputs = (AMP_WK, bathyZ, Tperiod)
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
    AMP_WK = parsed_features['AMP_WK']
    AMP_WK = tf.io.parse_tensor(AMP_WK, out_type=tf.float32)
    AMP_WK = tf.reshape(AMP_WK, [1,1])
    
    Tperiod = parsed_features['Tperiod']
    Tperiod = tf.io.parse_tensor(Tperiod, out_type=tf.float32)
    Tperiod = tf.reshape(Tperiod, [1,1])
    
    # Create tuple THIS NEEDS TO BE A TUPLE FOR CONSISTENT OUTPUTS
    inputs = (AMP_WK, bathyZ, Tperiod)
    outputs = asy
    
    return inputs, outputs

def parse_function3(tf_record_files,feature_description):
    dataset = tf.data.TFRecordDataset(tf_record_files)
    dataset = dataset.map(lambda proto: _parse_function(proto,feature_description))
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
    AMP_WK = parsed_features['AMP_WK']
    AMP_WK = tf.io.parse_tensor(AMP_WK, out_type=tf.float32)
    AMP_WK = tf.reshape(AMP_WK, [1,1])
    
    Tperiod = parsed_features['Tperiod']
    Tperiod = tf.io.parse_tensor(Tperiod, out_type=tf.float32)
    Tperiod = tf.reshape(Tperiod, [1,1])
    
    # Dummy output
    dummy_output = tf.concat([skew, AMP_WK, Tperiod], axis=0) 
    print("Shape of dummy_output:", dummy_output.shape)
    # Create tuple THIS NEEDS TO BE A TUPLE FOR CONSISTENT OUTPUTS
    inputs = (AMP_WK, bathyZ, Tperiod)
    outputs = dummy_output
    
    return inputs, dummy_output

def parse_function_dummy2(tf_record_files,feature_description):
    dataset = tf.data.TFRecordDataset(tf_record_files)
    dataset = dataset.map(lambda proto: _parse_function_dummy(proto,feature_description))
    return dataset
