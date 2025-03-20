import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code
from dotenv import load_dotenv
import os


# Define the design matrix
matrix_file = '/work/thsu/rschanta/RTS-PY/CIEG_682/BASE/Try2/design_matrices/RIP.csv'
#load_dotenv(r'C:/Users/rschanta/OneDrive - University of Delaware - o365/Desktop/Research/FUNWAVE_DS/FUNWAVE_DS/CIEG_682/BASE/Try1/envs/Try1.env')

# Pipeline: Get bathy_df, make stable
function_sets = {'Standard' : [mod.get_hydro,
                               mod.get_stable_grid,
                               mod.set_bathy,
                               mod.set_FW_params]}


# Plot functions
plot_functions = [mod.make_surf_plot,
                  mod.plot_cross_shore_slices,
                  mod.plot_long_shore_slices,
                  mod.make_contour_plot]

# Filter functions
filter_functions = []

# Print functions
print_functions = [fs.print_bathy]


# Write the files
fpy.process_design_matrix_NC(matrix_file, 
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')

