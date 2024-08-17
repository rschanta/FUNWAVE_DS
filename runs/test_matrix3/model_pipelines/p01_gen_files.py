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
    matrix_path = "/work/thsu/rschanta/RTS-PY/runs/test_matrix3/design_matrix/matrix_new.csv"
    matrix = fpy.load_FW_design_matrix(matrix_path)

    # Define functions to apply
    function_set = {'Regular' : [mod.stability_vars,
                          mod.get_bathy2,
                          mod.set_alt_title]}

    
    # Extra values to add (paths of the Dune3 data files)
    data_path = "/work/thsu/rschanta/RTS-PY/data/D3Data"
    extra_values = {'bathy_path': fpy.get_all_paths_in_path(data_path)}
    
    # Write the files
    fpy.write_files(matrix, function_set, super_path, run_name,extra_values)
    
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

