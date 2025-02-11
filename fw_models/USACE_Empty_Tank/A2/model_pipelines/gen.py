import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code

# Define the design matrix
matrix_file = '/work/thsu/rschanta/RTS-PY/fw_models/USACE_Empty_Tank/A2/design_matrices/A2.csv'

# Pipeline: Get bathy_df, make stable
function_sets = {'Standard' : [mod.get_input_vars,
                               mod.get_hydro,
                               mod.set_domain,
                               mod.set_stations]}


# Plot functions
plot_functions = []

# Filter functions
filter_functions = []

# Print functions
print_functions = [fs.print_stations]


# Write the files
fpy.process_design_matrix_NC(matrix_file, 
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')