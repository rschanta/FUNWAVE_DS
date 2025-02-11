import xarray as xr
import pandas as pd

def get_bathy_spectra_df(var_dict):
    # Unpack Variables-------------------------------------------------
    DATA_DIR = var_dict['DATA_DIR']
    D3_TRIAL = var_dict['D3_trial']
    #-----------------------------------------------------------------

    ## BATHYMETRY
    # Get information from filtered data (X and Z)
    filt_path = f'{DATA_DIR}/filtered/Trial{int(D3_TRIAL):02}.nc'
    ds_filt = xr.open_dataset(filt_path)[["X_before", "bed_num_before"]]
    # Get information from raw data (MWL)
    raw_path = f'{DATA_DIR}/raw/Trial{int(D3_TRIAL):02}.nc'
    ds_raw = xr.open_dataset(raw_path)[["MWL"]]
    # Adjust to height and return
    v_ref = ds_raw['MWL'].values[0] 
    df_bathy = pd.DataFrame({'X': ds_filt['X_before'].values,
                    'Z': v_ref - ds_filt['bed_num_before'].values})
    

    ## SPECTRA
    ds_eta = xr.open_dataset(filt_path)[["eta_i"]]
    # Start and end times
    t0 = ds_eta.attrs['t0']
    t_end = ds_eta.attrs['t_end']
    # Subset time range and select only the first loc_x
    eta_1 = ds_eta['eta_i'].sel(t=slice(t0, t_end), loc_x=ds_eta.loc_x[0])
    # Get into DataFrame
    df_spectra_ts = pd.DataFrame({'t': eta_1.coords['t'].values,
                'eta': eta_1.values})

    return {'df_bathy': df_bathy,
            'df_spectra_ts': df_spectra_ts}