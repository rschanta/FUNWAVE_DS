import numpy as np
import pandas as pd
from dataclasses import dataclass
import xarray as xr

"""
Contains subclasses of a NETCDF xarray useful for FUNWAVE
"""

class DomainObject2(xr.Dataset):
    __slots__ = ()


    def __init__(self, var_dict):

        # Construct X and Y coordinates from input parameters
        X = var_dict['DX'] * np.arange(0, var_dict['Mglob'])
        Y = var_dict['DY'] * np.arange(0, var_dict['Nglob'])
        print('X & Y shape')
        print(X.shape)
        print(Y.shape)

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

    # Method to define bathymetry from a custom 1D array, with Y tiling to 3 
    def z_from_1D_array(self, array):
        """Get Z from a 1D array, which will be tiled along the Y-axis."""

        if np.reshape(array, -1).shape[0] == self.attrs['Mglob']:
            # Tile the array along Y
            bathy_array = np.tile(array, (self.attrs['Nglob'], 1)).T
            self['Z'] = (('X', 'Y'), bathy_array)  # Adding Z as a DataArray with 'X' and 'Y' dimensions
            
        else:
            raise ValueError(f"Array dimensions {array.shape} do not match expected "
                             f"dimension: ({self.attrs['Mglob']})")

    # If using SLP and DEP_FLAT, construct the relevant bathymetry
    def z_from_dep_flat(self,vars):
        """Construct bathymetry from the depth flat case."""

        D = vars['DEPTH_FLAT']
        Xslp = vars['Xslp']
        SLP = vars['SLP']

        # Attributes
        DX = self.attrs['DX']
        Mglob = self.attrs['Mglob']
        Nglob = self.attrs['Nglob']
        
        # Initialize Bathy array
        z = [D] * Mglob
        
        # Get indices of sloping portion
        indices = list(range(int(Xslp // DX), Mglob))
        
        # Add onto portion
        for i in indices:
            z[i] = D - SLP * (i - Xslp // DX) * DX
        
        print('Z shape')
        #print(z.shape)
        
        # Construct output dictionary
        # Tile the array along Y
        bathy_array = np.tile(z, (self.attrs['Nglob'], 1)).T
        print('array shape')
        print(bathy_array.shape)  # Output: (2, 3)
        self['Z'] = (('X', 'Y'), bathy_array)  # Adding Z as a DataArray with 'X' and 'Y' dimensions
        
