import pandas as pd
import pickle
from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_permutation(k, perm, variable_ranges, set_name, pipeline, p, print_inputs, print_sets, plot_sets):
    # Create dictionary for parameters and values in permutation
    var_dict = dict(zip(variable_ranges.keys(), perm))
    ptr = fpy.get_FW_tri_paths(tri_num=k)

    # Add iteration-dependent values
    var_dict['TITLE'] = f'input_{k:05}'
    var_dict['DEP_PARAM_PIPELINE'] = set_name
    var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
    var_dict['ITER'] = k

    # Add dependent parameters
    var_dict = add_dependent_values(var_dict, pipeline)

    # Apply filter functions, proceed if none fail
    failed_params = None
    if filter_sets is not None:
        failed_params = apply_filters(var_dict, filter_sets)

    # Proceed if no failures
    if failed_params is None:
        # Print supporting files if indicated
        if print_sets is not None:
            var_dict = print_supporting_file(var_dict, print_sets)

        # Plot supporting plots if indicated
        if plot_sets is not None:
            plot_supporting_file(var_dict, plot_sets)

        # Print input.txt files if indicated
        if print_inputs:
            print_input_file(var_dict, ptr)

        # Output individual trial data
        with open(ptr['i_file_pkl'], 'wb') as f:
            pickle.dump(var_dict, f)

        return var_dict, ptr['RESULT_FOLDER']  # Return results
    else:
        return None, failed_params  # Return None for failed

def write_files2(matrix, 
                  print_inputs=True,
                  function_sets=None, 
                  filter_sets=None,
                  print_sets=None, 
                  plot_sets=None, 
                  extra_values=None):
    
    ###########################################################
    # Setup
    ###########################################################
    make_FW_paths()
    p = get_FW_paths()

    complete_matrix = []
    all_dicts = {}
    filter_failures = pd.DataFrame()

    ###########################################################
    # Finding permutations of all variables
    ###########################################################
    variable_ranges = group_variables(matrix)

    # Add on extra values if provided
    if extra_values is not None:
        variable_ranges = add_extra_values(variable_ranges, extra_values)

    # Get all possible permutations
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))

    ###########################################################
    # Looping through all permutations
    ###########################################################
    k = 1
    with ProcessPoolExecutor() as executor:
        futures = []
        
        # Loop: Processing Pipeline
        for set_name, pipeline in function_sets.items():
            # Loop: Permutation of variables
            for perm in permutations:
                futures.append(executor.submit(process_permutation, k, perm, variable_ranges, set_name, pipeline, p, print_inputs, print_sets, plot_sets))
                k += 1

        # Handle results
        for future in as_completed(futures):
            result, folder_or_failed = future.result()
            if result is None:
                # Record failure if triggered
                filter_failures = pd.concat([filter_failures, folder_or_failed], ignore_index=True, sort=False)
                print(f'PERMUTATION DOES NOT PASS FILTER: SKIP')
            else:
                # Update summaries
                complete_matrix.append(pd.DataFrame([result]))
                all_dicts[f'tri_{k:05}'] = folder_or_failed
                print(f'SUCCESSFULLY PRINTED FILES FOR TRIAL: {k:05}')
                print('#########################################################')
                
    ###########################################################
    # Save summary files
    ########################################################### 
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_dicts, f)

    complete_matrix = pd.concat(complete_matrix, ignore_index=True, sort=False)
    complete_matrix.to_csv(p['Im'], index=False)

    # Save failures to CSV
    filter_failures.to_csv(p['If'], index=False)

    return
