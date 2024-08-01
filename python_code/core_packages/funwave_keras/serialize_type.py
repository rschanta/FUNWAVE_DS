import tensorflow as tf

def serialize_tensor(feature_dict,var: str ,tensor):
    '''
    Serializes a tensor (as a BytesList) and its shape (as an Int64List) to
    the feature_dict. Shape is serializes as `{var}_shape`
    
    ARGUMENTS
        - feature_dict (dict): dictionary we're storing serialized features to,
            can be empty or contain others
        - var (str): name of the variable being serialized (ie- 'eta')
        - tensor (np.array): tensor to serialize
    RETURNS
        - feature_dict (dict): feature dictionary with the serialized tensor
            added

    '''
    feature_dict[f'{var}_shape'] = tf.train.Feature(int64_list=tf.train.Int64List(value=list(tensor.shape)))
    feature_dict[var] = tf.train.Feature(bytes_list=tf.train.BytesList(value=[tf.io.serialize_tensor(tensor).numpy()]))
    return feature_dict

def serialize_int(feature_dict,var: str, integer: int):
    '''
    Serializes an integer (as a int64_list) to the feature_dict. 
    
    ARGUMENTS
        - feature_dict (dict): dictionary we're storing serialized features to,
            can be empty or contain others
        - var (str): name of the variable being serialized (ie- 'Mglob')
        - tensor (int): value of the integer
    RETURNS
        - feature_dict (dict): feature dictionary with the serialized int
            added

    '''
    feature_dict[var] =  tf.train.Feature(int64_list=tf.train.Int64List(value=[integer]))
    return feature_dict

def serialize_float(feature_dict,var: str,floating_point_num):
    '''
    Serializes an float (as a FloatList) to the feature_dict. Should be a 
    float32 for consistency
    
    ARGUMENTS
        - feature_dict (dict): dictionary we're storing serialized features to,
            can be empty or contain others
        - var (str): name of the variable being serialized (ie- 'DX')
        - floating_point_num (float): value of the float
    RETURNS
        - feature_dict (dict): feature dictionary with the serialized float
            added

    '''
    feature_dict[var] =  tf.train.Feature(float_list=tf.train.FloatList(value=[floating_point_num]))
    return feature_dict

def serialize_string(feature_dict,var: str,value: str):
    '''
    Serializes an string (as a BytesList) to the feature_dict. 
    
    ARGUMENTS
        - feature_dict (dict): dictionary we're storing serialized features to,
            can be empty or contain others
        - var (str): name of the variable being serialized (ie- 'DEPTH_TYPE')
        - value (float): value of the string
    RETURNS
        - feature_dict (dict): feature dictionary with the serialized string
            added

    '''
    feature_dict[var] =  tf.train.Feature(bytes_list=tf.train.BytesList(value=[value.encode()]))
    return feature_dict

def serialize_boolean(feature_dict,var,value):
    '''
    Serializes an boolean string of either 'T' or 'F' (as a BytesList) to the 
    feature_dict. Will NOT accept booleans! 
    
    ARGUMENTS
        - feature_dict (dict): dictionary we're storing serialized features to,
            can be empty or contain others
        - var (str): name of the variable being serialized (ie- 'VISCOSITY_BREAKING')
        - value (string): either 'T' or 'F'
    RETURNS
        - feature_dict (dict): feature dictionary with the serialized string
            added
    '''
    if isinstance(var, bool):
        raise TypeError("The value must be a string, either 'T' or 'F.")
    else:
        feature_dict[var] =  tf.train.Feature(bytes_list=tf.train.BytesList(value=[value.encode()]))
    return feature_dict

