import xarray as xr
import os


def load_DUNE3_data(var_dict):
    '''
    Load in the data from Dune 3
    '''
    # Base path
    base_path  = r'C:\Users\rschanta\DATABASE\Dune 3\Net_CDF'
    load_dict = {}
    
    # Loop through Trials (5,24)
    for num in range(5,25):
        # Load In
        dsf = xr.load_dataset(os.path.join(base_path,'filtered',f'Trial{num:02}.nc'))
        dsr = xr.load_dataset(os.path.join(base_path,'raw',f'Trial{num:02}.nc'))
        
        # Initialize dictionary per trial
        tri_dict = {}
        
        # RAW DATA ----------------------------------------------
        # WG_loc_x: Location of the wave gages in X
        tri_dict['r_WG_loc_x'] = dsr['WG_loc_x'].values
        
        # X_before: X coordinate for bathymetry before
        tri_dict['r_X_before'] = dsr['X_before'].values
        # X_after: X coordinate for bathymetry after
        tri_dict['r_X_after'] = dsr['X_after'].values
        
        # ADV X coordinates
        tri_dict['r_ADV_X'] = dsr['ADV_X'].values
        tri_dict['r_ADV_Y'] = dsr['ADV_Y'].values
        tri_dict['r_ADV_Z'] = dsr['ADV_Z'].values
        
        # t: time
        tri_dict['r_t'] = dsr['t'].values
        tri_dict['r_t0'] = dsr.attrs['t0']
        tri_dict['r_t_end'] = dsr.attrs['t_end']

        # Bathymetry
        tri_dict['r_bed_before'] = dsr['bed_before'].values
        tri_dict['r_bed_after'] = dsr['bed_after'].values

        # Eta
        tri_dict['r_eta'] = dsr['eta'].values
        
        # MWL
        tri_dict['r_MWL'] = dsr['MWL'].values

        # Velocities
        tri_dict['r_u'] = dsr['u'].values
        tri_dict['r_v'] = dsr['v'].values
        tri_dict['r_w'] = dsr['w'].values
        # RAW DATA ----------------------------------------------



        # FILTERED DATA ----------------------------------------------
        tri_dict['f_loc_x'] = dsf['loc_x'].values
        
        # X_before: X coordinate for bathymetry before
        tri_dict['f_X_before'] = dsf['X_before'].values
        # X_after: X coordinate for bathymetry after
        tri_dict['f_X_after'] = dsf['X_after'].values

        # t: time
        tri_dict['f_t'] = dsf['t'].values
        tri_dict['f_t0'] = dsf.attrs['t0']
        tri_dict['f_t_end'] = dsf.attrs['t_end']

        # Bathymetry
        tri_dict['f_bed_before'] = dsf['bed_num_before'].values
        tri_dict['f_bed_num_after'] = dsf['bed_num_after'].values

        # Eta
        tri_dict['f_eta'] = dsf['eta'].values
        tri_dict['f_eta_i'] = dsf['eta_i'].values
        tri_dict['f_eta_r'] = dsf['eta_r'].values

        # Tsai Values
        tri_dict['omega'] = dsf['omega'].values
        tri_dict['a'] = dsf['a'].values
        tri_dict['theta'] = dsf['theta'].values
        tri_dict['k'] = dsf['k'].values
        # FILTERED DATA ----------------------------------------------


        # Append on to trial
        load_dict[f'tri_{num:02}'] = tri_dict
        
        
    return {'data': load_dict}
    