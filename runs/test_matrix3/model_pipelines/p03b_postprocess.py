import argparse
import os 
import sys
import tensorflow as tf
import pickle

def main(super_path,run_name):
    ## Get modules
    sys.path.append("/work/thsu/rschanta/RTS-PY")
    sys.path.append(f"/work/thsu/rschanta/RTS-PY/runs/{run_name}")
    
    # Import needed functions
    import funwave_ds.fw_py as fpy
    import funwave_ds.fw_tf as ftf
    import ml_models as ml
    
    # Directory where all the inputs are store
    directory = '/work/thsu/rschanta/RTS-PY/runs/test_matrix3/processed_outputs/ML_inputs'

    # Get all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    paths = sorted(files)

    ## Parse in features to dictionary
    tensors_2D = ['bathyX','bathyZ','skew','AMP_WK','Tperiod','asy']
    parsed_dict = ftf.parse_spec_var(paths,
                tensors_2D = tensors_2D,
                strings = ['ALT_TITLE','TITLE'])
    

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