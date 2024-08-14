import argparse
import os 
import sys
import tensorflow as tf


def main(super_path, run_name,tri_num):
    # Get necessary packages
    sys.path.append("/work/thsu/rschanta/RTS-PY")
    
    # Import needed functions
    import python_code as pc
    
    ## Construct path to processed output trial
    paths= [f'{super_path}/{run_name}/outputs-proc/out_{tri_num:05}.tfrecord']
    
    ## Parse in features to dictionary
    parsed_dict = pc.co.ke.parse_spec_var(paths,
                tensors_3D = ['eta'],
                tensors_2D = ['bathy','time_dt'],
                floats = ['DX','Xc_WK','AMP_WK','Tperiod'],
                strings = ['ALT_TITLE'])


    ## Apply post-processed features
    out_dict =  pc.ml.ska_conv.preprocessing_pipeline(parsed_dict,0)

    ## Serialize the post-processed features
    feature_dict_ML = pc.co.ke.serialize_all(out_dict)
    
    ## Save out 
    pc.co.ke.save_tfrecord(feature_dict_ML,f'/work/thsu/rschanta/RTS-PY/runs/test_matrix2/processed_outputs/ML_inputs/MLin_{tri_num:05}.tfrecord')

    
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