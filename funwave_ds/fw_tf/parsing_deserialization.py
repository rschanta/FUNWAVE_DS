import tensorflow as tf
from typing import  Dict, Any
from .feature_description import *


def deserialize_tensor(parsed_features,var:str):
    shape = tf.cast(parsed_features[f'{var}_shape'], tf.int64)
    tensor = tf.io.parse_tensor(parsed_features[var], out_type=tf.float32)
    parsed_features[var] = tf.reshape(tensor, shape)
    return parsed_features


def _parse_function(proto,feature_description,tensors):
    '''
    The actual parsing function, wrapped by `parse_function` to go from
    a dataset to a parsed dataset. Must specify which entries are tensors
    in order to convert to correct shape
    
        ARGUMENTS:
            - proto (Example protobuf): protobuf of type Example
            - feature_description (dict): feature description of all params.
            - tensors (list): list of params that are tensors
        RETURNS:
            - parsed_features (dict): dictionary of parsed features
    '''
    parsed_features = tf.io.parse_single_example(proto, feature_description)
    
    # Apply additional processing to tensors
    for var in tensors:
        parsed_features = deserialize_tensor(parsed_features,var)
        
    return parsed_features


def parse_function(tf_record_files,
                    feature_description,
                    tensors,out_type='dataset',
                    parse_fx = _parse_function):
    '''
    Wrapper function for a parsing function: parses all the files in 
    tf_record_files. Defaults to _parse_function, but can specify others.
    Must specify which entries are tensors in order to convert to correct shape. 
    Can output either as a parsed dataset, or as a human readable dictionary
    
        ARGUMENTS:
            - tf_record_files (list): list of tfrecord files
            - feature_description (dict): feature description of all params.
            - tensors (list): list of params that are tensors
            - out_type (string): either 'dataset' or 'dict' to set whether 
                a dataset or dictionary is the desired output (default: dataset)
            - parse_function: parsing function to use, defaults to `_parse_function`
                any substitutes should have the same function signature
        RETURNS:
            - p (dict): dictionary of parsed features
    '''
    dataset = tf.data.TFRecordDataset(tf_record_files)
    dataset = dataset.map(lambda proto: parse_fx(proto,feature_description,tensors))
    
    # Return just the dataset
    if out_type == 'dataset':
        return dataset
    # Return a dictionary, potentially nested
    elif out_type == 'dict':
        
        all_parsed_dict = {}
        
        for idx, parsed_features in enumerate(dataset):
            
            parsed_dict = {}
            
            for key, value in parsed_features.items():
                numpy_value = value.numpy()
                parsed_dict[key] = numpy_value
                
            #all_parsed_dict[parsed_dict['TITLE'].decode('utf-8')] = parsed_dict
            all_parsed_dict[parsed_dict[idx].decode('utf-8')] = parsed_dict
            
        # Deal with case of just 1 in the dataset 
        if len(tf_record_files) == 1:
            #all_parsed_dict = all_parsed_dict[parsed_dict['TITLE'].decode('utf-8')]
            all_parsed_dict = all_parsed_dict[parsed_dict[idx].decode('utf-8')]
            
        return all_parsed_dict
    else:
        raise ValueError("Specify either dataset or dict for out_type")
    

    return all_parsed_dict


## GOOD ONE: KEEP
def parse_spec_var(paths,
                tensors_4D = [],
                tensors_3D = [],
                tensors_2D = [],
                floats = [],
                strings = [],
                ints = []):



    # Ensure that Title is there
    strings = strings + ['TITLE']
    
    # Build up Feature Description
    feature_description = construct_feature_descr(tensors_4D, tensors_3D, tensors_2D, floats, strings, ints)
    
    # Specify the tensors
    tensors = tensors_4D + tensors_3D + tensors_2D
    
    # Transform into dataset and parse
    dataset = tf.data.TFRecordDataset(paths)
    dataset = dataset.map(lambda proto: _parse_function(proto,feature_description,tensors))
    
    # Loop through all returns in the dataset
    all_records_dictionary = {}
    k = 1
    for idx, parsed_features in enumerate(dataset):
        # Loop through the features in one record 

        record_dictionary = {}
        for key, value in parsed_features.items():

            value = value.numpy()
            record_dictionary[key] = value
            if isinstance(value, bytes):

                value = value.decode('UTF-8')
                record_dictionary[key] = value

        # Get title
        title = record_dictionary['TITLE']
        
        #new_key = title[-5:].decode('UTF-8')
        new_key = title[-5:]
        new_key = f'tri_{new_key}'
        all_records_dictionary[new_key] = record_dictionary
        k + 1
    return all_records_dictionary


'''
This might still be useful one day?
def get_tfrecord_as_dict(tensors_3d,tensors_2d,others,In_d,keys_to_ignore,tri_num,paths):
    # Construct feature description
    feature_description = get_feature_desc_tensors(tensors_3d, 3,{})
    feature_description = get_feature_desc_tensors(tensors_2d, 2,feature_description)
    feature_description = get_feature_desc_inputs(In_d[f'tri_{tri_num:05}'],feature_description)
    feature_description = add_features_manually(others,feature_description)

    # Remove extra keys
    feature_description_filt = {}
    for k, v in feature_description.items():
        if k not in keys_to_ignore:
            feature_description_filt[k] = v

    # Parse and return dict
    tensors = tensors_3d + tensors_2d
    return parse_function(paths,feature_description_filt,tensors,out_type='dict')
'''
