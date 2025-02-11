import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code

# Define the design matrix
matrix_file = '/work/thsu/rschanta/RTS-PY/fw_models/n2025/D3/design_matrices/D3.csv'

# Pipeline: Get bathy_df, make stable
function_sets = {'Standard' : [mod.get_bathy_spectra_df,
                               fs.set_WK_TIME_SERIES,
                               fs.set_stable_1D_bathy_data]}


# Plot functions
plot_functions = [fs.plot_1D_bathy,
                  fs.plot_WK_TIME_SERIES]

# Filter functions
filter_functions = []

# Print functions
print_functions = [fs.print_bathy,
                   fs.print_WK_TIME_SERIES_SPECTRA]


# Write the files
fpy.process_design_matrix_NC(matrix_file, 
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')