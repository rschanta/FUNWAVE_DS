# In-module imports
from ..utils import print_input_file
from .add_params import add_dependent_values,add_required_params, add_load_params
from .filter import apply_filters
from ..net_cdf import get_net_cdf
from ..configs import get_key_dirs
from .save_out import  print_supporting_file, plot_supporting_file,save_out_summary
from .combinations import find_combinations


#%%
def process_design_matrix_NC(matrix_csv=None, 
                            matrix_dict=None,
                            print_inputs = True,
                            load_sets = None,
                            function_set = None, 
                            filter_sets = None,
                            print_sets = None, 
                            plot_sets = None,
                            summary_formats = ['parquet','csv']):
    
    '''
    Works through the design matrix process
        - Loads in and checks data from either csv or dictionary
        - Finds all possible combinations of parameters (cartesian product)
        - Loads in any other data that should be accesible (load_vars)
        - Loops through each possible combination
            - Merge each combination with load_vars
            - add on dependent values from pipeline
            - add on required parameters
            - apply filtering conditions
    '''


    ## Initialization
    fail_data,pass_data = [],[] 
    k = 1                       
    
    ## Load in design matrix, parse variables, and group
    df_permutations = find_combinations(matrix_csv= matrix_csv,
                                        matrix_dict= matrix_dict)


    ## Load in data that should only be loaded once
    if load_sets:
        load_vars = add_load_params({},load_sets)

    #------------------------ Beginning of Loop-----------------------------#   
    for perm_i, row in df_permutations.iterrows():
        print(f'\nStarted processing permutation: {perm_i:05}...',flush=True)
        # Keep track of the combination index, regardless if it fails
        combo_num = perm_i + 1

        # Convert row to dictionary form
        var_dict = row.to_dict()

        # Merge with load set
        if load_sets:
            var_dict = {**var_dict, **load_vars}
    
        ## Add on dependent parameters
        var_dict = add_dependent_values(var_dict,function_set)
        
        ## Filtering conditions
        failed_params = apply_filters(var_dict,filter_sets)      
        
        # Failure Cases:
        if failed_params is not None:
            # Add on required parameters (just combo num)
            failed_params['COMBO_NUM'] = combo_num
            # Append to list
            fail_data.append(failed_params)
            print(f'Combination {combo_num:05} FAILED. Moving on.')
    
        ## No failures: proceed to output
        elif failed_params is None:    
            ##  Add on required parameters
            var_dict = add_required_params(var_dict,k,combo_num)
            
            # Create files other than input.txt 
            if print_sets:                                                                                    
                var_dict = print_supporting_file(var_dict,print_sets)
                
            # Output plots for visualization of input
            if plot_sets:                                               
                plot_supporting_file(var_dict,plot_sets)

            # Create xarray
            ds = get_net_cdf(var_dict)       

            ## Print `input.txt` for this given trial
            if print_inputs:
                print_input_file(ds.attrs)
                
            # Get data for summary
            pass_data.append(ds.attrs)

            ## End loop iteration
            print(f'SUCCESSFULLY PRINTED FILES FOR TRIAL: {k:05}',flush=True)
            print('#'*40)
            k = k + 1
       
    #------------------------ End of Loop-------------------------------

    ## Save out summaries
    df_pass,df_fail = save_out_summary(pass_data,fail_data,summary_formats)
    print('FILE GENERATION SUCCESSFUL!')
    return df_pass,df_fail
