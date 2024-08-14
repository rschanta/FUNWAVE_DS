import argparse
import sys
import os

## Import module with generation function

## Main: Generate the function
def main(super_path, run_name):
    # Path Commands
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp

    # Run Function
    trial_path = '../data/'  
    fp.mr.test1.generate_in(super_path,run_name,trial_path)
    print('File Generation Script Run!')
    return

#%%
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

