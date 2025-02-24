import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code

# Define the design matrix
matrix_file = '/work/thsu/rschanta/RTS-PY/fw_models/ENUD3/G2/design_matrices/G2.csv'

# Dependent Parameters
function_sets = {'Standard' : [mod.get_pickle_data,
                               mod.get_bathy,
                               mod.set_pi_vars]}


# Plot functions
plot_functions = [fs.plot_1D_bathy]

# Filter functions
filter_functions = []

# Print functions
print_functions = [fs.print_bathy]


# Write the files
fpy.process_design_matrix_NC2(matrix_file, 
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')