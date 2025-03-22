import os
from dotenv import load_dotenv
import sys
import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools

# Section if running just script
#sys.path.append(r'/work/thsu/rschanta/RTS-PY/test_runs/d2')
#load_dotenv(r'/work/thsu/rschanta/RTS-PY/test_runs/d2/envs/Try1.env')


#%%
import model_code as mod         # Model specific code


# Get the dictinoary of design matrix values
inputs = mod.design_matrix()

# Function Sets
function_set = [mod.get_hydro,
                mod.get_grid,
                mod.make_bar_channel_bathy,
                mod.set_stuff]


# Plot functions
plot_functions = [mod.make_surf_plot]

# Filter functions
filter_functions = [mod.filter_kh]

# Print functions
print_functions = [fs.print_bathy]


# Write the files
df_pass,df_fail = fpy.process_design_matrix_NC(matrix_dict = inputs,
                                    function_set = function_set, 
                                    filter_sets = filter_functions,
                                    plot_sets = plot_functions,
                                    print_sets = print_functions,
                                    summary_formats = ['parquet','csv'])

print('File Generation Script Run!')


