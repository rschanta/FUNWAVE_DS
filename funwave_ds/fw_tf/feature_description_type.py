import tensorflow as tf

def get_feature_desc_tensors(tensor_vars, dimensions,feature_description):
    
    '''
    Returns the feature description dictionary for all of the arrays/tensors
    specified in the list `tensor_vars`, as a string (bytes). Also returns
    the shape assuming {var}_shape notation for `dimensions` 
    
    ARGUMENTS:
        - tensor_vars (List[str]): lists of tensor variables
        - dimensions (int): number of dimensions for ALL tensors in tensor_vars
        - feature_description (dict): feature description dictionary to add to
    RETURNS:
        - feature_description (dict): feature description dict 
    
    '''
    for name in tensor_vars:
        feature_description[f'{name}_shape'] = tf.io.FixedLenFeature([dimensions], tf.int64)
        feature_description[f'{name}'] = tf.io.FixedLenFeature([], tf.string)

    return feature_description

def get_feature_desc_strings(string_vars,feature_description):
    
    '''
    Returns the feature description dictionary for all of the arrays/tensors
    specified in the list `tensor_vars`, as a string (bytes). Also returns
    the shape assuming {var}_shape notation for `dimensions` 
    
    ARGUMENTS:
        - string_vars (List[str]): lists of string variables
        - dimensions (int): number of dimensions for ALL tensors in tensor_vars
        - feature_description (dict): feature description dictionary to add to
    RETURNS:
        - feature_description (dict): feature description dict 
    
    '''
    for name in string_vars:
        feature_description[f'{name}'] = tf.io.FixedLenFeature([], tf.string)

    return feature_description


def get_feature_desc_floats(float_vars,feature_description):
    
    '''
    Returns the feature description dictionary for all of the floats
    specified in the list `float_vars`, as a string (bytes). 
    
    ARGUMENTS:
        - float_vars (List[str]): lists of float variables
        - dimensions (int): number of dimensions for ALL tensors in tensor_vars
        - feature_description (dict): feature description dictionary to add to
    RETURNS:
        - feature_description (dict): feature description dict 
    
    '''
    for name in float_vars:
        feature_description[f'{name}'] =  tf.io.FixedLenFeature([],tf.float32)

    return feature_description

def get_feature_desc_ints(int_vars,feature_description):
    
    '''
    Returns the feature description dictionary for all of the floats
    specified in the list `float_vars`, as a string (bytes). 
    
    ARGUMENTS:
        - int_vars (List[str]): lists of int variables
        - dimensions (int): number of dimensions for ALL tensors in tensor_vars
        - feature_description (dict): feature description dictionary to add to
    RETURNS:
        - feature_description (dict): feature description dict 
    
    '''
    for name in int_vars:
        feature_description[f'{name}'] =  tf.io.FixedLenFeature([],tf.int64)

    return feature_description