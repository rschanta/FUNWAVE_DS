import os
from dotenv import load_dotenv
import sys
import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
sys.path.append(r'C:/Users/rschanta/OneDrive - University of Delaware - o365/Desktop/Research/FUNWAVE_DS/FUNWAVE_DS/DUNE3/Base_Study')
import model_code as mod
from dotenv import load_dotenv
import os
load_dotenv(r'C:/Users/rschanta/OneDrive - University of Delaware - o365/Desktop/Research/FUNWAVE_DS/FUNWAVE_DS/DUNE3/Base_Study/pipe/work/DUNE3/Base_Study/envs/BASE1.env')
# Get the dictinoary of design matrix values
inputs = mod.design_matrix_D3_base()


# Load sets
load_set = [mod.load_DUNE3_data]

# Function Sets
function_set = [mod.get_spectra,
                mod.get_bathy_data,
                mod.get_hydro,
                mod.get_bathy]


# Plot functions
plot_functions = [mod.plot_spectra,mod.plot_domain]

# Filter functions
filter_functions = [] 

# Print functions
print_functions = [fs.print_bathy,
                   fs.print_WK_TIME_SERIES]


# Write the files
df_pass,df_fail = fpy.process_design_matrix_NC(matrix_dict = inputs,
                                               load_sets= load_set,
                                                function_set = function_set, 
                                                filter_sets = filter_functions,
                                                plot_sets = plot_functions,
                                                print_sets = print_functions,
                                                summary_formats = ['parquet','csv'])

print('File Generation Script Run!')


