import tensorflow as tf
from pathlib import Path


def save_tfrecord(feature_dict,file_name: str):
    '''
    Saves a .tfrecord file for the serialized feature_dict specified to 
    file_name
    
    ARGUMENTS:
        -feature_dict (dict): dictionary of all features to serialize and 
            save to the tfrecord file
        - file_name (str): Path to save to, as a string
    '''
    with tf.io.TFRecordWriter(file_name) as writer:
        example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
        writer.write(example.SerializeToString())
    return