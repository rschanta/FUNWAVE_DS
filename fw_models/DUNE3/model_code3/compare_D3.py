
'''
plot_process
    - Get the paths to the pickled data of Dune 3 Runs 5-24
        and pull out the bathymetry and MWL from the files
'''

import os
import matplotlib.pyplot as plt
import numpy as np
import pickle
import funwave_ds.fw_py as fpy

def compare_D3(vars):
    print('\t\tStarted plotting the process...')


    
    # Unpack Variables
    pickle_file = vars['pickle_file']
    WG = vars['adjusted_WG']
    X_FW = vars['bathy_array'][:,0]
    Z_FW = vars['bathy_array'][:,1]
    eta = vars['eta']
    t_FW = vars['time_dt'][:,0]
    ITER = vars['ITER']

    # Make folder if it doesn't exist
    p = fpy.get_FW_paths()
    folder_path = f'{p["RN_perm"]}/comparisons/tri_{ITER:05}'
    os.makedirs(folder_path, exist_ok=True)

    # Get Real Data
    with open(pickle_file, 'rb') as file:
        D3_real = pickle.load(file)

    

    #%% Find the indices closest to the point
    indices = np.argmin(np.abs(X_FW[:, np.newaxis] - WG), axis=0)
    eta_WG = eta[:,1,indices]
    eta_WG = eta_WG[:,0:14]


    t = D3_real['raw_data']['t'][5000:10000] - 50
    eta_real = D3_real['raw_data']['eta'][5000:10000,0:14]
    plt.close()
    # Plot
    """     for GAGE in range(1,13):
            plt.plot(t,eta_real[:,GAGE],label='Experimental')
            plt.plot(t_FW,eta_WG[:,GAGE],label='FUNWAVE')
            plt.grid()
            plt.xlabel('time (s)')
            plt.ylabel('$\eta$ (m)')
            plt.title(f'Dune 3 Trial {ITER}\nTrial {GAGE}')
            plt.show() 
    """
    for GAGE in range(0,14):
        fig,axs=plt.subplots(2,1,figsize=(10,6))
        
        ## Time Series Plot
        axs[0].plot(t,eta_real[:,GAGE],label='Experimental')
        axs[0].plot(t_FW,eta_WG[:,GAGE],label='FUNWAVE')
        axs[0].grid()
        axs[0].set_xlabel('time (t)')
        axs[0].set_ylabel('$\eta$ (m)')
        axs[0].legend(loc=4, ncol=2)
        axs[0].set_title('Time Series')
        
        ## Bathymetry
        axs[1].plot(X_FW,-Z_FW,label='Bathymetry',color='k')
        axs[1].grid()
        axs[1].set_xlabel('X (m)')
        axs[1].set_ylabel('z (m)')
        axs[1].axvline(x=WG[GAGE], color='r', linestyle='--', linewidth=2,label='Position of Time Series')
        axs[1].axhline(y=0, color='k', linestyle='--', linewidth=2,label='Datum')
        axs[1].legend(loc=4, ncol=2)
        axs[1].set_title('Domain')
        fig.tight_layout()
        
        ## Saving
        plt.savefig(f'{folder_path}/gage_{GAGE:02}.png', dpi=300, bbox_inches='tight')
        
        # Close and exit
        plt.close()

    
    print(f'\t\tSuccessfully plotted data!')
    return {}



