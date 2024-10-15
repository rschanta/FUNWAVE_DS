import argparse
import sys
import os
import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs     # Common function set tools
import model_code as mod         # Model specific code



# Load in Design Matrix
matrix = fpy.load_FW_design_matrix()

# Dependent Parameters
function_sets = {'Standard' : [mod.get_stability_vars,
                                mod.get_pi_vars,
                                mod.add_bathy]}

# Filter functions
filter_functions = [mod.filter_kh]

# Plot functions
plot_functions = [mod.plot_bathy]

# Print functions

# Write the files
fpy.write_files2(matrix, 
                function_sets = function_sets, 
                plot_sets = plot_functions,
                filter_sets = filter_functions)

print('\nFile Generation Script Run!')



