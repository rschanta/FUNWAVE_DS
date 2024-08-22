import argparse
import sys
import os



# Get modules
import funwave_ds.fw_py as fpy
sys.path.append("/work/thsu/rschanta/RTS-PY/fw_models/Dune3c")
import model_code as mod

# Load in Design Matrix
matrix = fpy.load_FW_design_matrix2()

# Dependent Parameters
function_sets = {'Pipeline' : [mod.get_pickle_path,
                                mod.get_spectra,
                                mod.stability_vars,
                                mod.get_bathy,
                                mod.get_TMA]}

# Extra Parameters

# Filter Functions

# Print functions
print_functions = [mod.print_bathy]

# Plot functions
plot_functions = [mod.plot_bathy, mod.plot_TS_spectra]

# Write the files
fpy.write_files3(matrix, 
                function_sets = function_sets, 
                print_sets = print_functions, 
                plot_sets = plot_functions)

print('File Generation Script Run!')



