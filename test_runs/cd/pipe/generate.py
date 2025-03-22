import os
from dotenv import load_dotenv
import sys
import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools

# Section if running just script
sys.path.append(r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS\test_runs\cd')
load_dotenv(r'C:/Users/rschanta/OneDrive - University of Delaware - o365/Desktop/Research/FUNWAVE_DS/FUNWAVE_DS/test_runs/cd/pipe/work/cd/envs/Try1.env')
import model_code as mod         # Model specific code


# Get the dictinoary of design matrix values
inputs = mod.design_matrix()


# Function Sets
function_set = [mod.get_hydro,
                mod.set_spatial_domain,
                mod.set_forcing,
                mod.set_friction,
                mod.set_stations]


# Plot functions
plot_functions = []

# Filter functions
filter_functions = [mod.filter_kh]

# Print functions
print_functions = [fs.print_bathy,
                   fs.print_friction,
                   fs.print_stations]


# Write the files
df_pass,df_fail = fpy.process_design_matrix_NC(matrix_dict = inputs,
                                    function_set = function_set, 
                                    filter_sets = filter_functions,
                                    plot_sets = plot_functions,
                                    print_sets = print_functions,
                                    summary_formats = ['parquet','csv'])

print('File Generation Script Run!')


