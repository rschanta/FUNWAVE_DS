import numpy as np
import pandas as pd
from dataclasses import dataclass
import xarray as xr

"""
Contains subclasses of a NETCDF xarray useful for FUNWAVE
"""
'''
class DomainObject2(xr.Dataset):
    __slots__ = ()


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
        
        # Initialize Bathy array
        z = [D] * Mglob
        
        # Get indices of sloping portion
        indices = list(range(int(Xslp // DX), Mglob))
        
        # Add onto portion
        for i in indices:
            z[i] = D - SLP * (i - Xslp // DX) * DX
        
        # Construct output dictionary
        # Tile the array along Y
        bathy_array = np.tile(z, (self.attrs['Nglob'], 1)).T

        self['Z'] = (('X', 'Y'), bathy_array)  # Adding Z as a DataArray with 'X' and 'Y' dimensions


'''



class DomainObject3(xr.Dataset):
    __slots__ = ()

    ## INITIALIZE =========================================================
    def __init__(self, DX=None,
                       DY=None,
                       Mglob=None,
                       Nglob=None):

        # Construct X and Y coordinates from input parameters
        X = DX * np.arange(0, Mglob)
        Y = DY * np.arange(0, Nglob)

        # Initialize the xarray Dataset with coordinates
        super().__init__(coords={'X': X, 
                                 'Y': Y})
        
        # Store important spatial parameters as attributes
        self.attrs['Mglob'] = Mglob
        self.attrs['Nglob'] = Nglob
        self.attrs['DX'] = DX
        self.attrs['DY'] = DY
    ## [END] INITIALIZE =========================================================


    ## ADD BATHYMETRY =========================================================    
    # DEPTH_TYPE = SLOPE 
    def z_from_SLOPE(self,
                        DEPTH_FLAT = None,
                        Xslp = None,
                        SLP = None):
        
        '''
        Construct the bathymetry from the DEPTH_TYPE = SLOPE Case. Note that this
        will automatically tile the 1D array constructed in the cross-shore to 
        whatever Nglob is set as.
        '''

        # Attributes
        DX = self.attrs['DX']
        Mglob = self.attrs['Mglob']
        

        # Initialize Bathy array
        z = [DEPTH_FLAT] * Mglob
        
        # Get indices of sloping portion
        indices = list(range(int(Xslp // DX), Mglob))
        
        # Add onto portion
        for i in indices:
            z[i] = DEPTH_FLAT - SLP * (i - Xslp // DX) * DX
        
        # Construct output dictionary
        # Tile the array along Y
        bathy_array = np.tile(z, (self.attrs['Nglob'], 1)).T

        self['Z'] = (('X', 'Y'), bathy_array)  
        return
    
    # DEPTH_TYPE = FLAT 
    def z_from_FLAT(self,
                DEPTH_FLAT = None):
        '''
        Construct the bathymetry from the DEPTH_TYPE = FLAT Case. Note that this
        will automatically tile the 1D array constructed in the cross-shore to 
        whatever Nglob is set as.
        '''

        # Attributes
        DX = self.attrs['DX']
        Mglob = self.attrs['Mglob']
        
        # Create array
        z = [DEPTH_FLAT] * Mglob
        
        bathy_array = np.tile(z, (self.attrs['Nglob'], 1)).T

        self['Z'] = (('X', 'Y'), bathy_array)  
        return
    
    # DEPTH_TYPE = DATA (1D) 
    def z_from_1D_array(self, bathy_array_1D):
        '''
        Construct the bathymetry from the DEPTH_TYPE = DATA Case. The input
        is a 1D array, that will be tiled along Nglob, which should at a 
        minimum be 3
        '''

        # First, check that it is indeed 1D and Mglob-dimensional
        if np.reshape(bathy_array_1D, -1).shape[0] == self.attrs['Mglob']:
            # Tile the array along Y
            bathy_array = np.tile(bathy_array_1D, (self.attrs['Nglob'], 1)).T
            # Add to object as a data variable
            self['Z'] = (('X', 'Y'), bathy_array)  
            
        else:
            raise ValueError(f"Array dimensions {bathy_array_1D.shape} do not match expected "
                             f"dimension: ({self.attrs['Mglob']})")
        return
    
    # DEPTH_TYPE = DATA (2D) 
    def z_from_2D_array(self, bathy_array_2D):
        '''
        Construct the bathymetry from the DEPTH_TYPE = DATA Case. The input
        is a 2D array.
        '''

        self['Z'] = (('X', 'Y'), bathy_array_2D)  
            
        return
    ## [END] ADD BATHYMETRY =========================================================


    ## ADD FRICTION =================================================================
    # DEPTH_TYPE = DATA (1D) 
    def friction_from_1D_array(self, friction_array_1D):
        '''
        Construct the friction matrix for a 1D simulation.
        '''

        # First, check that it is indeed 1D and Mglob-dimensional
        if np.reshape(friction_array_1D, -1).shape[0] == self.attrs['Mglob']:
            # Tile the array along Y
            bathy_array = np.tile(friction_array_1D, (self.attrs['Nglob'], 1)).T
            # Add to object as a data variable
            self['friction'] = (('X', 'Y'), bathy_array)  
            
        else:
            raise ValueError(f"Array dimensions {friction_array_1D.shape} do not match expected "
                             f"dimension: ({self.attrs['Mglob']})")
        return


    ## [END] ADD FRICTION ============================================================


    ## ADD STATIONS =================================================================
    def add_stations(self,
                     Mglob_pos=None,
                     Nglob_pos=None):
        """Add stations to a domain"""
        # Add GAGE_NUM as a new dimension
        self.coords['GAGE_NUM'] =  np.arange(len(Mglob_pos)) + 1

        # Add Mglob_pos and Nglob_pos as variables along GAGE_NUM
        self['Mglob_gage'] = (('GAGE_NUM'), Mglob_pos)
        self['Nglob_gage'] = (('GAGE_NUM'), Nglob_pos)
    ## [END] ADD STATIONS ============================================================


