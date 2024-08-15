import argparse
import sys
import os


## Main: Generate the function
def main(super_path, run_name):
    # Path Commands
    sys.path.append("/work/thsu/rschanta/RTS-PY")
    
    # Import needed functions
    import python_code as pc
    import python_code.model_runs.test2 as tri

    # Load in Design Matrix
    matrix_path = "/work/thsu/rschanta/RTS-PY/runs/test_matrix3/design_matrix/matrix_new.csv"
    matrix = pc.co.py.load_FW_design_matrix(matrix_path)

    # Define functions to apply
    function_set = {'Regular' : [tri.stability_vars,
                          tri.get_bathy2,
                          tri.set_alt_title]}

    
    # Extra values to add (paths of the Dune3 data files)
    data_path = "/work/thsu/rschanta/RTS-PY/data/D3Data"
    extra_values = {'bathy_path': pc.co.py.get_all_paths_in_dir(data_path)}
    
    # Write the files
    pc.co.py.write_files(matrix, function_set, super_path, run_name,extra_values)
    
    print('File Generation Script Run!')
    return


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

