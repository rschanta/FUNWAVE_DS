import argparse
import sys
import os

#test2.stability_vars({})
#%%
## Import module with generation function

## Main: Generate the function
def main(super_path, run_name):
    # Path Commands
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp

    # Load in Design Matrix
    matrix_path = r"C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\FUNWAVE_PY\data\matrices\matrix3.csv"
    matrix = fp.py.load_FW_design_matrix(matrix_path)
    
    # Define functions to apply
    functions_to_apply = [fp.mr.t2.stability_vars,
                          fp.mr.t2.get_bathy2,
                          fp.mr.t2.set_alt_title]
    
    # Extra values to add (paths of the Dune3 data files)
    data_path = r"C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\FUNWAVE_PY\data\Dune3"
    extra_values = {'bathy_path': fp.py.get_all_paths_in_dir(data_path)}
    
    # Write the files
    fp.py.write_files(matrix, functions_to_apply, super_path, run_name,extra_values)
    

    print('File Generation Script Run!')
    return

super_path = '../local_lustre/'
run_name = 'test_matrix'
main(super_path,run_name)
#%%
'''
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
'''
