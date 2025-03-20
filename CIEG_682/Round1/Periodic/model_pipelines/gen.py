import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code
from dotenv import load_dotenv

#%% Define the Inputs
inputs = {
    "Title": {
        "TITLE": {"CON": "DYNAMIC"}
    },

    "Parallel Info": {
        "PX": {"CON": "8"},
        "PY": {"CON": "4"}
    },

    "Depth": {
        "DEPTH_TYPE": {"CON": "DATA"}
    },

    "Dimension": {
        "Mglob": {"CON": "DYNAMIC"},
        "Nglob": {"CON": "DYNAMIC"}
    },

    "Time": {
        "TOTAL_TIME": {"CON": "150.0"},
        "PLOT_INTV": {"CON": "0.1"},
        "PLOT_INTV_STATION": {"CON": "0.1"},
        "SCREEN_INTV": {"CON": "10.0"}
    },

    "Grid": {
        "DX": {"CON": "DYNAMIC"},
        "DY": {"CON": "DYNAMIC"}
    },

    "Wavemaker": {
        "WAVEMAKER": {"CON": "WK_REG"},
        "Tperiod": {"LIST": ["5.0","9.0"]},
        "Xc_WK": {"CON": "DYNAMIC"},
        "AMP_WK": {"CON": "0.5"},
        "DEP_WK": {"CON": "DYNAMIC"},
        "Yc_WK": {"CON": "0.0"},
        "Theta_WK": {"LIST": ["0.0" ,"5.0","10.0","15.0","20.0"]},
        "Delta_WK": {"CON": "3.0"}
    },

    "Periodic Boundary Condition": {
        "PERIODIC": {"CON": "T"}
    },

    "Sponge Layer": {
        "DIFFUSION_SPONGE": {"CON": "F"},
        "FRICTION_SPONGE": {"CON": "T"},
        "DIRECT_SPONGE": {"CON": "T"},
        "Csp": {"CON": "0.0"},
        "Cdsponge": {"CON": "1.0"},
        "Sponge_south_width": {"CON": "0.0"},
        "Sponge_north_width": {"CON": "0.0"},
        "Sponge_west_width": {"CON": "DYNAMIC"},
        "Sponge_east_width": {"CON": "0.0"}
    },

    "Friction": {
        "Cd": {"CON": "0.0"}
    },

    "Numerics": {
        "CFL": {"CON": "0.5"},
        "FroudeCap": {"CON": "3.0"}
    },

    "Wet-Dry": {
        "MinDepth": {"CON": "0.01"},
        "VISCOSITY_BREAKING": {"CON": "T"}
    },

    "Breaking": {
        "Cbrk1": {"CON": "0.65"},
        "Cbrk2": {"CON": "0.35"}
    },

    "Wave Averaging": {
        "T_INTV_mean": {"CON": "160.0"},
        "STEADY_TIME": {"CON": "160.0"}
    },

    "Output": {
        "FIELD_IO_TYPE": {"CON": "BINARY"},
        "DEPTH_OUT": {"CON": "T"},
        "ETA": {"CON": "T"},
        "MASK": {"CON": "T"},
        "U": {"CON": "T"},
        "V": {"CON": "T"},
        "WAVEHEIGHT": {"CON": "F"},
        "OUT_NU": {"CON": "F"},
        "UNDERTOW": {"CON": "T"},
        "ROLLER": {"CON": "T"}
    },

    "Custom Inputs": {
            "h_offshore": {"CON": "8.0"},        
            "h_onshore": {"CON": "1.0"},         
            "s": {"CON": "0.0333"},              
            "bar_depth": {"CON": "1.0"},         
            "bar_height": {"CON": "2.0"},        
            "bar_width": {"CON": "60.0"},       
            "channel_depth": {"CON": "2.0"},     
            "channel_width": {"CON": "10.0"},   
            "beach_LS_width": {"CON": "DYNAMIC"},   
            "T_bar": {"CON": "True"},
            "T_slp": {"CON": "True"},
            "T_cha": {"CON": "True"},
    },

    "Custom Nondimensional Inputs": {
        "PI_W": {"CON": "1.5"},
        "PI_D": {"CON": "1.0"},
        "PI_F": {"CON": "1.0"},
        "PI_S": {"CON": "0.0"},
        "PI_N": {"CON": "0.0"},
    },
    
}

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
