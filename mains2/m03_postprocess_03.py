import argparse
import os 
import sys
import tensorflow as tf


def main(super_path, run_name,tri_num):
    ## Get modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp
    
    ## Construct path to processed output trial
    paths= [f'{super_path}/{run_name}/outputs-proc/out_{tri_num:05}.tfrecord']
    
    ## Parse in features to dictionary
    parsed_dict = fp.tf.parse_spec_var(paths,
                tensors_3D = ['eta'],
                tensors_2D = ['bathy','time_dt'],
                floats = ['DX','Xc_WK','AMP_WK','Tperiod'],
                # TODO: figure out why strings aren't working
                strings = ['ALT_TITLE'])


    ## Apply post-processed features
    out_dict =  fp.ml.ska_conv.preprocessing_pipeline(parsed_dict,0)

    ## Serialize the post-processed features
    feature_dict_ML = fp.tf.serialize_all(out_dict)
    
    ## Save out 
    fp.tf.save_tfrecord(feature_dict_ML,f'{super_path}/{run_name}/inputs-ML/MLin_{tri_num:05}.tfrecord')

    
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