
import os
import sys
import funwave_ds.fw_fs as ffs
import funwave_ds.fw_py as fpy

sys.path.append(r'C:/Users/rschanta/OneDrive - University of Delaware - o365/Desktop/Research/FUNWAVE_DS/FUNWAVE_DS/DUNE3/Base_Study')
import model_code as mod

var_dict = {'D3_Trial': 5, 
            'PI_1': 1,
            'PI_2': 3.0,
            'PI_3': 1.5,
            'PI_4': 0.1,
            'T_lower': 2,
            'T_higher': 40}

var_dict ={**var_dict, **mod.load_DUNE3_data({})}  

var_dict = {**var_dict, **mod.get_spectra(var_dict)}
var_dict = {**var_dict, **mod.get_bathy_data(var_dict)}
var_dict = {**var_dict, **mod.get_hydro(var_dict)}
var_dict = {**var_dict, **mod.get_bathy(var_dict)}


#%% Spectra plot
import matplotlib.pyplot as plt
import numpy as np

def plot_domain(var_dict):
    # Unpack ---------------------------------------------------------------------
    Xc_WK = var_dict['Xc_WK']
    D3_Trial = var_dict['D3_Trial']
    X = var_dict['DOM'].X.values
    Z = var_dict['DOM'].Z.values[:,1]
    Sponge_west_width = var_dict['Sponge_west_width']
    # Unpack ---------------------------------------------------------------------
    
    # Find coast
    i_coast = np.argmin(np.abs(Z))
    X_wet = X[:i_coast]
    Z_wet = Z[:i_coast]
    
    # Find sponge and wavemaker
    end_sponge_i = np.argmin(np.abs(X-Sponge_west_width))
    WK_i = np.argmin(np.abs(X-Xc_WK))
    X_blue = X[WK_i:i_coast]
    Z_blue = Z[WK_i:i_coast]
    
    fig,ax = plt.subplots(dpi=300,figsize=(10,4))
    # Plot the bathymetry, shade beach under
    ax.plot(X,-Z,color='black')
    ax.fill_between(X,-Z,-Z[0]*np.ones(len(X)),color='goldenrod')
    
    # Plot the original flume
    ax.fill_between(X_blue,-Z_blue,np.zeros(len(Z_blue)),color='cadetblue',label= 'Actual Flume')
    
    
    ax.plot(X_wet,np.zeros(len(X_wet)),color='blue')
    ax.plot([Xc_WK,Xc_WK],[-Z[0],0.5],color='red')
    
    ax.text(
        Xc_WK, 0.5, "WK", 
        ha='center', va='bottom',  # horizontal & vertical alignment
        fontsize=10,
        bbox=dict(boxstyle="circle", edgecolor='black', facecolor='white')
    )
    ax.fill_between([0,Sponge_west_width],
                    [-Z[0],-Z[0]], 
                    [0,0],color='green',alpha=0.5,label= 'Sponge')
    ax.fill_between([Sponge_west_width,Xc_WK],
                    [-Z[0],-Z[0]], [0,0],
                    color='purple',alpha=0.5,label= 'WK Room')
    ax.legend()
    ax.set_xlim(0,X[-1])
    ax.set_ylim(-Z[0],np.max(Z))
    ax.set_title(f'Dune 3 Trial {D3_Trial} Model Domain')
    
    return