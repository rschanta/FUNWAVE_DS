import numpy as np
import pandas as pd
from dataclasses import dataclass
import xarray as xr
#%% Variable along some coordinate
class CoordVar:
    def __init__(self,dimensions,value):
        self.dims = dimensions
        self.value = value
        
#%% NET-CDF Helper Classes
@dataclass
class CoordList:
    pass  
@dataclass
class VarList:
    pass  
@dataclass
class AttList:
    pass  
    

#%% HELPER FUNCTIONS
def add_attributes(obj, var_dict,param_list):
    ''' Adds the parameters in param_list to the attrs of obj'''
    for key in param_list:
        try:
            setattr(obj.attrs, key, var_dict[key])
        except:
            print(f'{key} not found in dictionary defaults (likely) used.')
            
            
#%% SUPERCLASS FOR COORDINATE OBJECTS
class CoordinateObject:
    def __init__(self, **coordinates):
        """Initialize with any number of named coordinates."""
        self.coords = CoordList()
        for name, value in coordinates.items():
            setattr(self.coords, name, value)
        self.vars = VarList()
        self.attrs = AttList()


#%% DOMAIN OBJECT SUBCLASS: for bathy, breakwater, friction, etc.
class DomainObject(CoordinateObject):
    def __init__(self, var_dict):
        
        # Construct X and Y from  FW input parameters
        X = var_dict['DX']*np.arange(0,var_dict['Mglob'])
        Y = var_dict['DY']*np.arange(0,var_dict['Nglob'])
        
        # Set X and Y as coordinates
        super().__init__(X=X, Y=Y)  
        
        # Important spatial parameters
        for key in ['Mglob', 'Nglob', 'DX', 'DY']:
            setattr(self.attrs, key, var_dict[key])
        

    # Define bathymetry from a custom array
    def z_from_array(self,array):
        ''' Get Z from an array '''
    
        # Ensure that it is dimensionally correct
        if np.shape(array) == (self.attrs.Mglob,self.attrs.Nglob):
            # Add a CoordVar to vars if so
            setattr(self.vars, 'Z', CoordVar(['X','Y'],array))
        else:
            raise ValueError(f"Array dimensions {array.shape} do not match expected "
                             f"dimensions ({self.attrs.Mglob}, {self.attrs.Nglob})")
        

    # Define bathymetry from a custom array
    def z_from_1D_array(self,array):
        ''' Get Z from an 1D array (ie- must be tiled to 3) '''
    
        # Ensure that it is dimensionally correct
        if np.reshape(array, -1).shape[0] == self.attrs.Mglob:
            # Add the artificial Y tiling
            bathy_file = np.tile(array, (3, 1)).T
            # Add a CoordVar 
            setattr(self.vars, 'Z', CoordVar(['X','Y'],bathy_file))
        else:
            raise ValueError(f"Array dimensions {array.shape} does not match expected "
                             f"dimension: ({self.attrs.Mglob})")
        

    # Construct bathymetry from DEP_FLAT
    def z_from_dep_flat(self):
        pass
        # TODO: construct bathymetry from the depth flat case
            

class DomainObject2(xr.Dataset):
    def __init__(self, var_dict):

        # Construct X and Y coordinates from input parameters
        X = var_dict['DX'] * np.arange(0, var_dict['Mglob'])
        Y = var_dict['DY'] * np.arange(0, var_dict['Nglob'])

        # Initialize the xarray Dataset with coordinates
        super().__init__(coords={'X': X, 'Y': Y})
        
        # Store important spatial parameters as attributes
        for key in ['Mglob', 'Nglob', 'DX', 'DY']:
            self.attrs[key] = var_dict[key]


    # Method to define bathymetry from a custom 2D array
    def z_from_array(self, array):
        """Get Z from an array and add it as a variable."""

        # Adding Z as a DataArray with 'X' and 'Y' dimensions
        if np.shape(array) == (self.attrs['Mglob'], self.attrs['Nglob']):
            self['Z'] = (('X', 'Y'), array)  
        else:
            raise ValueError(f"Array dimensions {array.shape} do not match expected "
                             f"dimensions ({self.attrs['Mglob']}, {self.attrs['Nglob']})")

    # Method to define bathymetry from a custom 1D array, with Y tiling
    def z_from_1D_array(self, array):
        """Get Z from a 1D array, which will be tiled along the Y-axis."""

        if np.reshape(array, -1).shape[0] == self.attrs['Mglob']:
            # Tile the array along Y
            bathy_array = np.tile(array, (self.attrs['Nglob'], 1)).T
            self['Z'] = (('X', 'Y'), bathy_array)  # Adding Z as a DataArray with 'X' and 'Y' dimensions
            
        else:
            raise ValueError(f"Array dimensions {array.shape} do not match expected "
                             f"dimension: ({self.attrs['Mglob']})")

    # Placeholder for constructing bathymetry from DEP_FLAT
    def z_from_dep_flat(self):
        """Construct bathymetry from the depth flat case."""
        pass  # Implementation of this method as needed


        
#%% DOMAIN OBJECT SUBCLASS: for bathy, breakwater, friction, etc.
class WavemakerObject(CoordinateObject):     
    def __init__(self, var_dict):
        super().__init__()
        
        # Set Wavemaker type
        WK = var_dict['WAVEMAKER']
        self.WAVEMAKER = WK

        # Basic Wave Makers
        if WK in {'WK_REG','WK_IRR','JON_2D','JON_1D','TMA_1D'}:
            
            # Basic Parameters
            add_attributes(self, var_dict,['Xc_WK', 'Yc_WK', 'Ywidth_WK', 'DEP_WK','Time_ramp'])
            
            # Regular Wave Maker
            if WK == 'WK_REG':
                add_attributes(self, var_dict ['Tperiod', 'AMP_WK', 'Theta_WK'])

            # Basic Spectral Parameters
            if WK in {'WK_IRR','JON_2D','JON_1D','TMA_1D'}:
                add_attributes(self, var_dict, ['Delta_WK', 'FreqPeak', 'FreqMin','FreqMax','Hmo','GammaTMA'])
            
            # 1D Spectral Parameters
            if WK in {'TMA_1D','JON_1D'}:
                add_attributes(self, var_dict, ['Nfreq'])     
                
            # 2D Spectral Parameters
            if WK in {'WK_IRR','JON_2D'}:
                add_attributes(self, var_dict, ['ThetaPeak', 'Nfreq', 'Ntheta'])

        # WK Time Series
        if WK == 'WK_TIME_SERIES':
            add_attributes(self, var_dict, ['WaveCompFile', 'NumWaveComp', 'DEP_WK','Xc_WK','Ywidth_WK'])
            
            
    def calc_time_series_1D(self,time=None,eta=None,lo=None,hi=None):
        
        assert None not in (time.any(), eta.any(), lo, hi)
        
        # Keep original time series data 
        self.coords.t_spectra = time
        self.vars.eta_spectra = CoordVar(['t_spectra'],eta)

        # Record cutoff frequencies
        self.attrs.f_cutoff_lo = lo
        self.attrs.f_cutoff_hi = hi
    
        # Calculate spectra
        dt = time[1]-time[0]     # time step
        N = len(eta)       # record length
        fft_values = np.fft.fft(eta) 
        freqs = np.fft.fftfreq(N, d=dt)
        
        # Cut to Nyquist
        freqs = freqs[:N//2]
        fft_values = fft_values[:N//2]
        
        # Amplitude and Phase at each frequency
        amp = 2*np.abs(fft_values) /N
        phase = -np.angle(fft_values)
        
        # Combine into dataframe
        df_spectra = pd.DataFrame({ 
                            'freqs': freqs,
                            'period': 1 /freqs,
                            'amplitude': amp,
                            'phase': phase
                            })
        
        df_spectra_cut = df_spectra[df_spectra['freqs'].between(lo, hi)]
        
        # Keep both spectral dataframes
        self.df_spectra = df_spectra
        self.df_spectra_cut = df_spectra_cut
        
        # Add spectra along a coordinate
        perr = df_spectra_cut['period'].to_numpy()
        ampp = df_spectra_cut['amplitude'].to_numpy()

        self.coords.period = df_spectra_cut['period']
        self.attrs.PeakPeriod = perr[np.argmax(ampp)]
        self.attrs.NumWaveComp = len(perr)
        self.vars.amp2 = CoordVar(['period'],df_spectra_cut['amplitude'])
        self.vars.phase2 = CoordVar(['period'],df_spectra_cut['phase'])
        return
    
    def add_1D_spectra(self,period=None,amplitude=None,phase=None):
        # Add some spectra with this information pre-calculated
        self.coords.per = period
        self.attrs.PeakPeriod = period[np.argmax(amplitude)]
        self.attrs.NumWaveComp = len(period)
        self.vars.amp = CoordVar(['per'],amplitude)
        self.vars.phase = CoordVar(['per'],phase)
        self.vars.theta = CoordVar(['per'],0*phase)
        return


#%%
import numpy as np

def add_coords(CoordObj,ds):
    # Coordinates are stored in CoordObj.coords: neglect __ python stuff
    for coord_name in dir(CoordObj.coords):
        if not coord_name.startswith('__'):
            # Assign the coordinates to ds
            coord_value = getattr(CoordObj.coords, coord_name)
            ds = ds.assign_coords({coord_name: (coord_name, coord_value)})
    return ds

def add_data_vars(CoordObj,ds):
    for var_name in dir(CoordObj.vars):
        if not var_name.startswith('__'):
            var_value = getattr(CoordObj.vars, var_name)
            # Create a new data variable using "assign"
            ds = ds.assign({var_name: 
                            (var_value.dims, var_value.value)
                            })
    return ds

def add_attr_vars(CoordObj,ds):
    for attr_name in dir(CoordObj.attrs):
        if not attr_name.startswith('__'):
            attr_value = getattr(CoordObj.attrs, attr_name)
            
            # Create a new data variable using "assign"
            ds.attrs[attr_name] = attr_value
    return ds

def is_valid_netcdf_attribute(var):
    valid_types = (str, int, float, np.int32, np.int64, np.float32, np.float64, np.ndarray)
    # Check if it's a string, int, or float, or a 1D array of numeric types
    if isinstance(var, valid_types):
        if isinstance(var, np.ndarray) and var.ndim == 1 and var.dtype.type in (np.int32, np.int64, np.float32, np.float64):
            return True
        elif not isinstance(var, np.ndarray):
            return True
    return False
