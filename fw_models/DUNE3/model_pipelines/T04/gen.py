import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code3 as mod         # Model specific code

# Define the design matrix
matrix_file = '/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/design_matrices/T03.csv'

# Dependent Parameters
function_sets = {'Standard' : [mod.get_pickle_data,
                               mod.get_spectra,
                               mod.get_period,
                               mod.get_bathy,
                               mod.set_pi_vars,
                               mod.plot_process]}


# Plot functions
plot_functions = [fs.plot_1D_bathy,
                 fs.plot_TS_spectra_new]

# Filter functions
filter_functions = [fs.filter_kh]

# Print functions
print_functions = [fs.print_bathy,
                   fs.print_TS_spectra_new]


# Write the files
fpy.process_design_matrix(matrix_file, 
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')