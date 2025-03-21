import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
# Section if running just script
import sys
sys.path.append('/work/thsu/rschanta/RTS-PY/test_runs/d2')

import model_code as mod         # Model specific code


# Get the dictinoary of design matrix values
inputs = mod.design_matrix()



# Function Sets
function_sets = {'Standard' : [mod.get_hydro,
                               mod.get_grid,
                               mod.make_bar_channel_bathy,
                               mod.set_stuff]}


# Plot functions
plot_functions = [mod.plot_long_shore_slices,
                  mod.make_surf_plot,
                  mod.plot_cross_shore_slices,
                  mod.make_contour_plot]

# Filter functions
filter_functions = []

# Print functions
print_functions = [fs.print_bathy]


# Write the files
fpy.process_design_matrix_NC('', 
                 matrix_dict = inputs,
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')