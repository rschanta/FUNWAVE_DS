import tensorflow as tf
from .feature_description_type import *

def construct_feature_descr(tensors_4D = [],
                            tensors_3D = [],
                            tensors_2D = [],
                            floats = [],
                            strings = ['TITLE'],
                            ints = []):
    
    feature_descriptions = get_feature_desc_tensors(tensors_4D, 4,{})
    feature_descriptions = get_feature_desc_tensors(tensors_3D, 3,feature_descriptions)
    feature_descriptions = get_feature_desc_tensors(tensors_2D, 2,feature_descriptions)
    feature_descriptions = get_feature_desc_floats(floats,feature_descriptions)
    feature_descriptions = get_feature_desc_strings(strings,feature_descriptions)
    feature_descriptions = get_feature_desc_ints(ints,feature_descriptions)

    return feature_descriptions

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