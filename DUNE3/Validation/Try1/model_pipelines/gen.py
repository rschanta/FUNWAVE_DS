# Import packages
from dotenv import load_dotenv
import funwave_ds.fw_py as fpy
import funwave_ds.fw_fs as ffs
import model_code as mod

# Matrix file
matrix_file = '/work/thsu/rschanta/RTS-PY/DUNE3/Validation/Try1/design_matrices/Try1.csv'
# Loading parameters
load_sets = [mod.load_DUNE3_data]

# Dependent Parameters
function_sets = {'Standard' : [mod.get_spectra,
                               mod.set_spectra,
                               mod.get_bathy,
                               mod.get_hydro,
                               mod.set_bathy]}


# Plot functions
plot_functions = [ffs.plot_1D_bathy,
                  ffs.plot_1D_TS_spectra]

# Filter functions
filter_functions = []

# Print functions
print_functions = [ffs.print_bathy,
                   ffs.print_WK_TIME_SERIES_SPECTRA]


# Write the files
fpy.process_design_matrix_NC(matrix_file, 
                load_sets = load_sets,
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')