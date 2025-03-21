import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import sys
sys.path.append(r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS\USACE\Flat_Tank\Cd_Study')
import model_code as mod         # Model specific code
from dotenv import load_dotenv

load_dotenv(r'C:/Users/rschanta/OneDrive - University of Delaware - o365/Desktop/Research/FUNWAVE_DS/FUNWAVE_DS/USACE/Flat_Tank/Cd_Study/envs/Cd_Study.env')

#%% Generation

inputs = {
    "Title": {
        "TITLE": {"CON": "DYNAMIC"}
    },

    "Parallel Info": {
        "PX": {"CON": "32"},
        "PY": {"CON": "1"}
    },

    "Depth": {
        "DEPTH_TYPE": {"CON": "FLAT"},
        "DEPTH_FLAT": {"LO": "1.0", "HI": "20.0", "NUM": "20"},
    },

    "Dimension": {
        "Mglob": {"CON": "DYNAMIC"},
        "Nglob": {"CON": "DYNAMIC"}
    },

    "Time": {
        "TOTAL_TIME": {"CON": "DYNAMIC"},
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
        "Tperiod": {"LO": "2.0","HI": "16.0","NUM": "15"},
        "Xc_WK": {"CON": "DYNAMIC"},
        "AMP_WK": {"CON": "DYNAMIC"},
        "DEP_WK": {"LO": "1.0", "HI": "1.0", "NUM": "20.0"},
        "Yc_WK": {"CON": "0.0"},
        "Theta_WK": {"CON": "0.0"},
        "Delta_WK": {"CON": "3.0"}
    },

    "Periodic Boundary Condition": {
        "PERIODIC": {"CON": "F"}
    },

    "Sponge Layer": {
        "DIFFUSION_SPONGE": {"CON": "F"},
        "FRICTION_SPONGE": {"CON": "T"},
        "DIRECT_SPONGE": {"CON": "T"},
        "Csp": {"CON": "0.0"},
        "Sponge_south_width": {"CON": "0.0"},
        "Sponge_north_width": {"CON": "0.0"},
        "Sponge_west_width": {"CON": "DYNAMIC"},
        "Sponge_east_width": {"CON": "DYNAMIC"}
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
        "U": {"CON": "F"},
        "V": {"CON": "F"},
        "WAVEHEIGHT": {"CON": "F"},
        "OUT_NU": {"CON": "F"},
        "UNDERTOW": {"CON": "F"},
        "ROLLER": {"CON": "F"}
    },

    "Custom Nondimensional Inputs": {
            "PI_1": {"CON": "4.0"},        
            "PI_2": {"CON": "1.0"},         
            "PI_3": {"CON": "50.0"},              
            "PI_4": {"CON": "100.0"},         
            "PI_5": {"CON": "4.0"},        
            "PI_6": {"CON": "60.0"},       
            "PI_7": {"CON": "2.0"},     
            "XI_1": {"CON": "0.05"},   
            "TAU_1": {"CON": "150.0"},   
    },
    
}


#%%
import funwave_ds.fw_py as fpy   # Basic functionality
import funwave_ds.fw_fs as fs    # Common function set tools
import model_code as mod         # Model specific code

# Define the design matrix
matrix_file = '/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Sens/design_matrices/DX_Sens.csv'

# Pipeline: Get bathy_df, make stable
function_sets = {'Standard' : [mod.get_hydro,
                               mod.set_domain,
                               mod.set_stations]}


# Plot functions
plot_functions = []

# Filter functions
filter_functions = [fs.filter_kh]

# Print functions
print_functions = [fs.print_stations]


# Write the files
fpy.process_design_matrix_NC('', 
                 matrix_dict = inputs,
                function_sets = function_sets, 
                filter_sets = filter_functions,
                plot_sets = plot_functions,
                print_sets = print_functions)

print('File Generation Script Run!')