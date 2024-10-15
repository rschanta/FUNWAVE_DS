import argparse
import sys
import os



# Get modules
import funwave_ds.fw_py as fpy
sys.path.append("/work/thsu/rschanta/RTS-PY/fw_models/Dune3c")
import model_code as mod

# Load in Design Matrix
matrix = fpy.load_FW_design_matrix2()

# Function Set
function_sets = {'Pipeline' : [mod.get_pickle_path,
                                mod.get_spectra,
                                mod.stability_vars,
                                mod.get_bathy,
                                mod.print_bathy,
                                mod.print_time_series_spectra_file,
                                mod.plot_bathy,
                                mod.plt_spectra]}

# Write the files
fpy.write_files2(matrix, 
                function_sets = function_sets)

print('File Generation Script Run!')



