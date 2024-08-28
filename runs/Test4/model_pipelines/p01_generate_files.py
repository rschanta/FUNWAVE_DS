import argparse
import sys
import os


## Main: Generate the function
def main(super_path, run_name):

    # Add to system path
    sys.path.append("/work/thsu/rschanta/RTS-PY")
    sys.path.append(f"/work/thsu/rschanta/RTS-PY/runs/{run_name}")
    # Get modules
    import funwave_ds.fw_py as fpy
    import model_code as mod

    # Load in Design Matrix
    matrix_path = "/work/thsu/rschanta/RTS-PY/runs/dep_flat_tma/design_matrices/Exploratory_1.csv"
    matrix = fpy.load_FW_design_matrix(matrix_path)

    # Function Set
    function_set = {'TMA' : [mod.stability_vars_1,
                          mod.beach_geometry_1,
                          mod.bathy_for_dep_flat]}

    # Write the files
    fpy.write_files(matrix, function_set, super_path, run_name,{})
    
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
