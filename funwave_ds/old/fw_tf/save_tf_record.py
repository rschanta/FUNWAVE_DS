import tensorflow as tf
from pathlib import Path
import os
import funwave_ds.fw_hpc as fba

def save_tfrecord(feature_dict):
    '''
    Saves a .tfrecord file for the serialized feature_dict specified to 
    file_name
    
    ARGUMENTS:
        -feature_dict (dict): dictionary of all features to serialize and 
            save to the tfrecord file
        - file_name (str): Path to save to, as a string
    '''
    d = fba.get_directories()
    path = os.path.join(d['DATA_DIR'],d['FW_MODEL'],d['RUN_NAME'],'fw_outputs')
    
    os.makedirs(path, exist_ok=True)
    tri_num = int(os.getenv('TRI_NUM'))

    filename = os.path.join(path,f'Out_{tri_num:05}.tfrecord')

    with tf.io.TFRecordWriter(filename) as writer:
        example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
        writer.write(example.SerializeToString())

    print(f'\nSuccessfully made: {filename}')
    return


def save_tfrecord2(feature_dict,path):
    '''
    Saves a .tfrecord file for the serialized feature_dict specified to 
    file_name
    
    ARGUMENTS:
        -feature_dict (dict): dictionary of all features to serialize and 
            save to the tfrecord file
        - file_name (str): Path to save to, as a string
    '''


    with tf.io.TFRecordWriter(path) as writer:
        example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
        writer.write(example.SerializeToString())

    print(f'\nSuccessfully made: {path}')
    return