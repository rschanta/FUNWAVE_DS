import argparse
import os 
import sys
import tensorflow as tf


def main(super_path, run_name,tri_num):
    # Get necessary packages
    sys.path.append("/work/thsu/rschanta/RTS-PY")
    
    # Import needed functions
    import python_code as pc
    
    ## Get paths
    p = pc.co.py.get_FW_paths(super_path, run_name)
    ptr = pc.co.py.get_FW_tri_paths(tri_num, p)
    paths = ptr['out_record']

    ## Parse in features to dictionary
    parsed_dict = pc.co.tf.parse_spec_var(paths,
                tensors_3D = ['eta'],
                tensors_2D = ['bathy','time_dt'],
                floats = ['DX','Xc_WK','AMP_WK','Tperiod'],
                strings = ['TITLE','ALT_TITLE'])

    ## Apply post-processed features
    out_dict =  pc.ml.ska_conv.preprocessing_pipeline3(parsed_dict[f'tri_{tri_num:05}'],0)

    ## Serialize the post-processed features
    feature_dict_ML = pc.co.tf.serialize_dictionary(out_dict,{})
    
    ## Save out 
    pc.co.tf.save_tfrecord(feature_dict_ML,f'/work/thsu/rschanta/RTS-PY/runs/test_matrix3/processed_outputs/ML_inputs/MLin_{tri_num:05}.tfrecord')

    
    return

if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Process variables for compression")
    
    # Add arguments and descriptions
    parser.add_argument("super_path", type=str, help="Path to super directory")
    parser.add_argument("run_name", type=str, help="Name of the run")
    parser.add_argument("tri_num", type=int, help="Trial number")
    
    # Call the parser
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.super_path, args.run_name,args.tri_num)