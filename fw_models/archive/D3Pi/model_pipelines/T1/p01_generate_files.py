import argparse
import sys
import os



# Get modules
import funwave_ds.fw_py as fpy
sys.path.append("/work/thsu/rschanta/RTS-PY/fw_models/D3Pi")
import model_code as mod

# Load in Design Matrix
matrix = fpy.load_FW_design_matrix()

# Dependent Parameters
function_sets = {'Standard' : [mod.get_pickle_data,
                               mod.get_spectra_data,
                               mod.get_period,
                                mod.get_bathy,
                                mod.get_pi_vars]}


# Plot functions
plot_functions = [mod.plot_bathy,mod.plot_TS_spectra]
print_functions = [mod.print_bathy,mod.print_TS_spectra]
# Write the files
fpy.write_files2(matrix, 
                function_sets = function_sets, 
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')



