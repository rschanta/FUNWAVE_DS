import xarray as xr
import os
def load_DUNE3_data(var_dict):
    # Base path
    base_path  = r'C:\Users\rschanta\DATABASE\Dune 3\Net_CDF'
    load_dict = {}
    
    for num in range(5,25):
        # Load In
        dsf = xr.load_dataset(os.path.join(base_path,'filtered',f'Trial{num:02}.nc'))
        dsr = xr.load_dataset(os.path.join(base_path,'raw',f'Trial{num:02}.nc'))
        
        # Initialize dictionary per trial
        tri_dict = {}
        
        # RAW DATA
        tri_dict['r_WG_loc_x'] = dsr['WG_loc_x'].values
        tri_dict['r_X_before'] = dsr['X_before'].values
        tri_dict['r_t'] = dsr['t'].values
        tri_dict['r_bed_before'] = dsr['bed_before'].values
        tri_dict['r_eta'] = dsr['eta'].values
        tri_dict['r_t0'] = dsr.attrs['t0']
        tri_dict['r_t_end'] = dsr.attrs['t_end']
        tri_dict['r_MWL'] = dsr['MWL'].values
        
        # FILTERED DATA
        tri_dict['f_loc_x'] = dsf['loc_x'].values
        tri_dict['f_X_before'] = dsf['X_before'].values
        tri_dict['f_t'] = dsf['t'].values
        tri_dict['f_bed_before'] = dsf['bed_num_before'].values
        tri_dict['f_eta'] = dsf['eta'].values
        tri_dict['f_eta_i'] = dsf['eta_i'].values
        tri_dict['f_eta_r'] = dsf['eta_r'].values
        tri_dict['f_t0'] = dsf.attrs['t0']
        tri_dict['f_t_end'] = dsf.attrs['t_end']
        
        # Append on to trial
        load_dict[f'tri_{num:02}'] = tri_dict
        
        
    return load_dict