import argparse
import os 
import sys
import tensorflow as tf
import pickle

def main(super_path,run_name):
    ## Get modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp
    
    # Directory where all the inputs are store
    directory = f'{super_path}/{run_name}/inputs-ML'

    # Get all files in the directory
    files = fp.py.get_all_paths_in_dir(directory)
    paths = sorted(files)

    ## Parse in features to dictionary
    tensors_2D = ['bathyX','bathyZ','skew','AMP_WK','Tperiod','asy']
    parsed_dict = fp.tf.parse_spec_var(paths,
                tensors_2D = tensors_2D,
                strings = ['ALT_TITLE'])
    

    ## Save out
    with open(f'{super_path}/{run_name}/inputs-proc/postprocessed.pkl', 'wb') as f:
        pickle.dump(parsed_dict, f)

if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Process variables for compression")
    
    # Add arguments and descriptions
    parser.add_argument("super_path", type=str, help="Path to super directory")
    parser.add_argument("run_name", type=str, help="Name of the run")
    
    # Call the parser
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.super_path, args.run_name)