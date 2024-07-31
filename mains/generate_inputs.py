import argparse
import sys
import os

## Import module with generation function

## Main: Generate the function
def main(super_path, run_name):
    # Path Setup
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../model_runs')))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../packages')))
    import time_spectra_a_f as ts

    
    # Run Function
    trial_path = '../data/Trial05.pkl'
    ts.generate_in(super_path,run_name,trial_path)
    
    # print
    print('File Generation Script Run!')
    return
#%% Test out


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

