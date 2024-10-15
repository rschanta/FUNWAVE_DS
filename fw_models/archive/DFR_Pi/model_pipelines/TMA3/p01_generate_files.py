import argparse
import sys
import os



# Get modules
import funwave_ds.fw_py as fpy
sys.path.append("/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi")
import model_code as mod

# Load in Design Matrix
matrix = fpy.load_FW_design_matrix()

# Dependent Parameters
function_sets = {'Standard' : [mod.get_period,
                               mod.get_stability_vars,
                                mod.get_pi_vars,
                                mod.add_bathy]}


# Plot functions
plot_functions = [mod.plot_bathy]

# Write the files
fpy.write_files2(matrix, 
                function_sets = function_sets, 
                plot_sets = plot_functions)

print('File Generation Script Run!')



