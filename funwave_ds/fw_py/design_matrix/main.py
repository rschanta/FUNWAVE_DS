import shutil


## NOTE: These must be here for compatibility reasons
from netCDF4 import Dataset
import h5py

# In-module imports
from ..configs import get_FW_paths, make_FW_paths,get_FW_tri_paths
from ..utils import print_input_file
from ..configs import save_logs_to_file
from .add_params import add_dependent_values,add_required_params, add_load_params
from .load import load_group_matrix
from .filter import apply_filters
from .save_out import make_pass_parquet, make_fail_parquet, print_supporting_file, plot_supporting_file
from ..net_cdf import get_net_cdf
from ..utils import print_input_file

def process_design_matrix_NC(matrix_file, 
                print_inputs = True,
                load_sets = None,
                function_sets = None, 
                filter_sets = None,
                print_sets = None, 
                plot_sets = None,
                start_row = None):
    
    '''
    Works through the design matrix process
    '''

    ## Paths needed
    make_FW_paths()
    p = get_FW_paths()
    
    ## Initialization
    fail_data,pass_data = {},{} # For valid and failed combinations
    k = 1                       # trial number counter
    
    ## Load in design matrix, parse variables, and group
    df_permutations = load_group_matrix(matrix_file,function_sets,p)

    ## Load in data that should only be loaded once
    if load_sets:
        load_vars = add_load_params({},load_sets)

    ## Adjust start row if set
    if start_row is not None:
        df_permutations = df_permutations.iloc[start_row:]

    #------------------------ Beginning of Loop-----------------------------#   
    for perm_i, row in df_permutations.iterrows():
        
        
        print(f'\nStarted processing permutation: {perm_i:05}...',flush=True)
        # Paths needed
        ptr = get_FW_tri_paths(tri_num=k)  
        # Get row as a dictionary
        var_dict = row.to_dict()

        # Merge in with the load set
        if load_sets:
            var_dict = {**var_dict, **load_vars}
    
        ## Add on dependent parameters
        pipe = function_sets[var_dict['PIPELINE']]
        var_dict = add_dependent_values(var_dict,pipe)

        ##  Add on others
        var_dict = add_required_params(var_dict,perm_i,ptr)
        
        ## Filtering conditions
        failed_params = apply_filters(var_dict,filter_sets)      
        
        if failed_params is not None:
            fail_data[f'trial_{perm_i:05}'] = failed_params
            print(f'Permutation {perm_i:05} failed. Moving on.')
    
        ## No failures: proceed to output
        elif failed_params is None:    
            # Progress iteration
            var_dict['ITER'] = k
            
            # Create files other than input.txt 
            if print_sets:                                                                                    
                var_dict = print_supporting_file(var_dict,print_sets)
                
            # Output plots for visualization of input
            if plot_sets:                                               
                plot_supporting_file(var_dict,plot_sets)

            # Create netcdf
            data_proc,non_cdf_stuff = get_net_cdf(var_dict,ptr)       

            ## Print `input.txt` for this given trial
            if print_inputs:
                print_input_file(data_proc.attrs,ptr)
                
            # Get data for summary
            pass_data[f'trial_{k:05}'] = data_proc

            ## End loop iteration
            print(f'SUCCESSFULLY PRINTED FILES FOR TRIAL: {k:05}')
            print('#'*40)
            k = k + 1
       
    #------------------------ End of Loop-------------------------------

    ## Save out failures and successes
    df_pass = make_pass_parquet(pass_data,p)     
    df_fail = make_fail_parquet(fail_data,p)


    # Save record of function calls (to logs)
    save_logs_to_file(f"{p['L']}/generation_function_log.py")
    save_logs_to_file(f"{p['L']}/generation_function_log.txt")

    # Save copy of design matrix (to logs)
    shutil.copy(matrix_file, f"{p['L']}/design_matrix.csv")

    return df_pass, fail_data
