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

def get_feature_desc_inputs(In_di,feature_description):
    '''
    Returns the feature description dictionary for all of the input variables
    in In_d input directory (excluding files)
    
    ARGUMENTS:
        - In_di (dict): the subdirectory of the master input dictionary 
            (ie- In_d['tri_00001'])
        - feature_description (dict): feature description dictionary to add to
    RETURNS:
        - feature_description (dict): feature description dict 
    
    '''
    for input_var,value in In_di.items():
        if isinstance(value, int):
            feature_description[input_var] = tf.io.FixedLenFeature([], tf.int64)
        elif isinstance(value, float):
            feature_description[input_var] = tf.io.FixedLenFeature([],tf.float32)
        elif isinstance(value, str):
            if value == 'files':
                pass
            else:
                feature_description[input_var] = tf.io.FixedLenFeature([], tf.string)
    return feature_description


def add_features_manually(small_feature_desc,feature_description):
    '''
    Appends a smaller dictionary of feature descriptions to a larger one 
    already made
    
    ARGUMENTS:
        - small_feature_desc (dict): smaller feature dictionary to add
        - feature_description (dict): feature description dictionary to add to
    RETURNS:
        - feature_description (dict): feature description dict 
    
    '''
    for key, value in small_feature_desc.items():
       feature_description[key] = value

    return feature_description