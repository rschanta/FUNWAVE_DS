import pandas as pd
import xarray as xr
import requests
from io import BytesIO
from datetime import datetime, timedelta
import numpy as np

#%%
def get_FRF_wave_data(date_str, 
                      date_format="%Y-%m-%d",
                      get_hour = None):
    '''
    Gets the data from https://chldata.erdc.dren.mil/thredds/catalog/frf/oceanography/waves/8m-array/catalog.html
    
    ARGUMENTS
        - date_str (string): string for the date
        - date_format (string): date format: default "%Y-%m-%d"
        
    RETURNS
        - dictionary with:
            - Dataframe for each unique timestep found in the database,
                specified as 
    '''

    ## Get parts of the date, ensure that it is valid
    try:
        # Datetime object
        date = datetime.strptime(date_str, date_format)
        # Get year, month, day
        year = date.year
        month = date.month
        day = date.day

    except ValueError:
        raise ValueError(f"Error: The date '{date_str}' is not a valid date.")
        return None

    ## Construct the url to FRF
    base_url = "https://chldata.erdc.dren.mil/thredds/fileServer/frf/oceanography/waves/8m-array/"
    base_file = "/FRF-ocean_waves_8m-array_"
    full_url = f"{base_url}{year}{base_file}{year}{month:02}.nc"
    
    
    ## TODO: DEAL WITH DATES THAT CANT BE FOUND
    '''
    IDEA: Search through each month of the year we're in
    '''
    
    ## Get the netcdf data into a dataframe
    response = requests.get(full_url)
    response.raise_for_status()  
    data = BytesIO(response.content)
    ds = xr.open_dataset(data)
    df = ds.to_dataframe()
    
    ## Index out just the specific date requested
    df = df.loc[date_str]
    
    ## Round times to nearest hour
    time_index = pd.to_datetime(df.index.get_level_values('time'))
    rounded_time_index = time_index.round('h')
    new_index = pd.MultiIndex.from_arrays([
        rounded_time_index,
        df.index.get_level_values('waveFrequency'),
        df.index.get_level_values('waveDirectionBins')
    ], names=['time', 'waveFrequency', 'waveDirectionBins'])
    df.index = new_index
    
    ## Get unique times, frequencies, and direction bins
    output_dict = {}
    times = df.index.get_level_values('time').unique()
    output_dict['_times'] = times.hour.to_numpy()
    output_dict['_frequency'] = df.index.get_level_values('waveFrequency').unique().to_numpy()
    output_dict['_directions'] = df.index.get_level_values('waveDirectionBins').unique().to_numpy()
    
    ## Get into dictionary
    
    for time in times:
        output_dict[f'H_{time.strftime("%H")}'] = df.loc[time]
        
    ## Get a specific time if found
    if get_hour is not None:
        try:
            output_df = output_dict[f'H_{get_hour}']
            return output_df
        except:
            closest_hour = output_dict['_times'][(np.abs(output_dict['_times'] - get_hour)).argmin()]
            output_df = output_dict[f'H_{closest_hour}']
            print(f'Could not find hour {get_hour}: Using closest hour of {closest_hour}')
            return output_df
    else:
        return output_dict


def get_FRF_bathy_data(date_str, 
                      date_format="%Y-%m-%d",
                      get_hour = None):
    '''
    Gets the data from https://chldata.erdc.dren.mil/thredds/catalog/frf/oceanography/waves/8m-array/catalog.html
    
    ARGUMENTS
        - date_str (string): string for the date
        - date_format (string): date format: default "%Y-%m-%d"
        
    RETURNS
        - dictionary with:
            - Dataframe for each unique timestep found in the database,
                specified as 
    '''

    ## Get parts of the date, ensure that it is valid
    try:
        # Datetime object
        date = datetime.strptime(date_str, date_format)
        # Get year, month, day
        year = date.year
        month = date.month
        day = date.day

    except ValueError:
        raise ValueError(f"Error: The date '{date_str}' is not a valid date.")
        return None

    ## Construct URL to FRF
    base_url = "https://chldata.erdc.dren.mil/thredds/fileServer/frf/geomorphology/elevationTransects/survey/data/"
    base_file = "FRF_geomorphology_elevationTransects_survey_"
    full_url = f"{base_url}{base_file}{year}{month:02}{day}.nc"
    
    ## Try getting the data:
    try:
        response = requests.get(full_url)
        response.raise_for_status()  
    except:
        print('Date selected not in FRF. Searching for next closest date...')
        
        for k in range(1,31):
            # Adjust date
            newdate = date + timedelta(days=k)
            day = newdate.day
            date_str = newdate.strftime('%Y-%m-%d')
            
            # Try the next day
            try:
                print(f'Trying: {newdate}')
                full_url = f"{base_url}{base_file}{year}{month:02}{day}.nc"
                response = requests.get(full_url)
                response.raise_for_status() 
                print(f'Successful! Using File for {newdate}')
                break
            except requests.exceptions.HTTPError as e:
                print(f'{newdate} data not found. Proceeding\n')
                if k == 31:
                    print('No close date after found: Try again.')
    
    ## Convert data into a dataframe
    data = BytesIO(response.content)
    ds = xr.open_dataset(data)
    df = ds.to_dataframe()

    ## Narrow down to specific date 
    df = df.loc[date_str]
    
    ## Refactor the profile number
    # Get unique profiles
    ProfileNumbers = sorted(df['profileNumber'].unique())
    # Create mapping from old profile numbers to new profile IDs
    mapping = {}
    for index, value in enumerate(ProfileNumbers):
        mapping[value] = index
    # Apply the mapping
    df['profile_ID'] = df['profileNumber'].map(mapping)
    
    ## Separate into separate profiles
    df_dict = {}
    for profile_ID in range(len(ProfileNumbers)):
        # Get each profile, sort by x value
        sub_df = df[df['profile_ID'] == profile_ID]
        sub_df = sub_df.sort_values(by='xFRF')
        df_dict[profile_ID] = sub_df
    
    ## Add metadata
    df_dict['_date'] = date_str
    
    return df_dict