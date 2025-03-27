import os
from dotenv import load_dotenv
import sys
import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code


# Get the dictinoary of design matrix values
inputs = mod.design_matrix_base_study()


# Function Sets
function_set = [mod.get_hydro,
                mod.set_spatial_domain,
                mod.set_forcing,
                mod.set_stations]


# Plot functions
plot_functions = []

# Filter functions
filter_functions = [mod.filter_kh,
                    mod.filter_L70]

# Print functions
print_functions = [fs.print_bathy,
                   fs.print_stations]


# Write the files
df_pass,df_fail = fpy.process_design_matrix_NC(matrix_dict = inputs,
                                    function_set = function_set, 
                                    filter_sets = filter_functions,
                                    plot_sets = plot_functions,
                                    print_sets = print_functions,
                                    summary_formats = ['parquet','csv'])

print('File Generation Script Run!')


