from .feature_description_type import *

def construct_feature_descr(tensors_3D = [],
                            tensors_2D = [],
                            floats = [],
                            strings = ['TITLE'],
                            ints = []):
    
    feature_descriptions = get_feature_desc_tensors(tensors_3D, 3,{})
    feature_descriptions = get_feature_desc_tensors(tensors_2D, 2,feature_descriptions)
    feature_descriptions = get_feature_desc_floats(floats,feature_descriptions)
    feature_descriptions = get_feature_desc_strings(strings,feature_descriptions)
    feature_descriptions = get_feature_desc_ints(ints,feature_descriptions)

    return feature_descriptions

