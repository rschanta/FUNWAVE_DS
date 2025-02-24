import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sys
sys.path.append(r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS\DUNE3\Validation\Try1')
import model_code as mod
import funwave_ds as fds


#%% Load in Data
#vard = fds.add_load_params({}, [mod.load_DUNE3_data])


#%% SPECTRA


'''
# Peak Amplitude
ATmax = max(amp)

fig,ax = plt.subplots(dpi=200)
ax.plot(T,amp)

ax.scatter(Tmax,ATmax,c='RED',zorder=3)
ax.set_xlim(0,75)

'''
#%%

r'''
num = 5
base_path  = 'C:\Users\rschanta\DATABASE\Dune 3\Net_CDF'
dsf = xr.load_dataset(os.path.join(base_path,'filtered',f'Trial{num:02}.nc'))
dsr = xr.load_dataset(os.path.join(base_path,'raw',f'Trial{num:02}.nc'))
'''
#%% PLOT OF DOMAIN AS-IS
'''
fig,ax = plt.subplots(dpi=200)
# Plot Wave Gauges from Raw Data
for k in range(len(dsr['WG_loc_x'])):
    if k == 0:
        ax.axvline(dsr['WG_loc_x'].values[k],
                   c='grey',ls='--',label='Wave Gauges')
    else:
        ax.axvline(dsr['WG_loc_x'].values[k],
                   c='grey',ls='--')

# Plot position of FILTERED eta values
for k in range(len(dsf['loc_x'])):
    if k == 0:
        ax.axvline(dsf['loc_x'].values[k],
                   c='lightsalmon',ls='--',label='Eta Pos')
    else:
        ax.axvline(dsf['loc_x'].values[k],
                   c='lightsalmon',ls='--')
    
  
    
ax.plot(dsr['X_before'],dsr['bed_before'],label='raw')
ax.plot(dsf['X_before'],dsf['bed_num_before'],label='filtered')
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
ax.grid()
ax.set_title('Dune 3 Trial 5')
 ''' 
#%% Try depth tools

def get_bathy(var_dict):
    # UNPACK FROM LOADED DATA ------------------
    # Get bathymetry
    tri_no = int(var_dict['D3_Trial'])
    X = var_dict[f'tri_{tri_no:02}']['f_X_before']
    Z = var_dict[f'tri_{tri_no:02}']['f_bed_before']


    ## ADD ON DISTANCE
    Xa,Za = fds.add_flat_distance(X,Z,5,side='left')
    
    ## INTERPOLATE TO GRID
    DX = 0.25
    Xb,Zb = fds.interpolate_align(Xa, Za, DX)

    return {'Xb': Xb,
            'Zb': Zb,
            'DX': DX}
#
#bathy_result  = get_bathy(vard)
'''
fig,ax = plt.subplots(dpi=200)
ax.plot(X,Z,
        c='black',label='Original')
ax.plot(Xa,Za,
        ls='--',c='red',label='Add distance')
ax.plot(Xb,Zb,
        ls='--',c='orange',label='Interpolate/Align')
ax.legend()
'''



#%%
import xarray as xr
path = r'C:/Users/rschanta/HPC_Pretend/DUNE3_Data/Validation/Try1/net_cdf/tri_00004.nc'

ds = xr.load_dataset(path)

import matplotlib.pyplot as plt
plt.plot(ds['X'] ,-ds['Z'])

plt.show()

plt.plot(ds['period'],ds['amp'])


