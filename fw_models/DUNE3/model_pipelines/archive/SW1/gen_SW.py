import sys
import os
import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code



# Load in Design Matrix
matrix_file = '/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/design_matrices/SW1.csv'
matrix = fpy.load_FW_design_matrix2(matrix_file)

# Dependent Parameters
function_sets = {'Standard' : [mod.get_pickle_data,
                               mod.get_bathy,
                               mod.set_pi_vars]}


# Plot functions
plot_functions = [fs.plot_1D_bathy]

# Filter functions
filter_functions = [fs.filter_kh]

# Print functions
print_functions = [fs.print_bathy]


# Write the files
fpy.write_files2(matrix, 
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')

