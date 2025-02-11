import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code

# Define the design matrix
matrix_file = '/work/thsu/rschanta/RTS-PY/fw_models/debug/A/design_matrices/A.csv'

# Dependent Parameters
function_sets = {'Standard' : [mod.set_params]}


# Plot functions
plot_functions = [fs.plot_1D_bathy]

# Filter functions
filter_functions = [mod.greater_kh]

# Print functions
print_functions = []


# Write the files
fpy.process_design_matrix_NC(matrix_file, 
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions,
                start_row = 5)

print('File Generation Script Run!')