

import pandas as pd


def add_var(df=None,var=None,const='CONST',value=None,lo=None,hi=None,num=None):
    # Create if no matrix given
    if df is None:
        df = pd.DataFrame(columns= ['VAR','CONST','VALUE','LO','HI','NUM'])
    # Error handling for column names
    elif set(df.columns) != set(['VAR','CONST','VALUE','LO','HI','NUM']):
        raise ValueError('Dataframe must have columns VAR, CONST, VALUE, LO, HI, NUM, and no others!')
        
    # Raise error for const
    if const not in {'CONST', 'RANGE'}:
        raise ValueError('Specify const as CONST or RANGE!')
        
    # Error handling for string type
    if var is None:
        raise TypeError('Must specify name of variable!')
    elif not isinstance(var,str):
        raise TypeError('Variable name must be a string!')
    
        
        
    if const == 'CONST':
        if value is None:
            raise TypeError('Must specify value for a constant!')
        
        df = pd.concat([pd.DataFrame([
            [var,       # Name of variable 
             'CONST',   # Specify as constant
             value,     # Constant value
             None,      # set rest to None
             None,
             None]
            ], columns=df.columns), df])
        
        
    elif const == 'RANGE':
        # Error handling
        if not isinstance(lo, float) and not isinstance(hi, float):
            raise TypeError('Lower and upper bounds must be floats!')
        if not isinstance(num,int):
            raise TypeError('Number of points must be an integer!')
            
        # Append onto range
        df = pd.concat([pd.DataFrame([
            [var,       # Name of variable 
             'RANGE',   # Specify as range
             None,     # Specify as None
             lo,      # lower bound
             hi,      # upper bound
             num]     # number of points
            ], columns=df.columns), df])
    else:
        raise ValueError('Must specify either const as either CONST or RANGE!')
        
    return df
       
#%% Define the input.txt file! 
matrix = add_var(var="AMP_WK",const='CONST',value=0.5)

# Processors
matrix = add_var(matrix, var="PX", const='CONST', value=16)
matrix = add_var(matrix, var="PY", const='CONST', value=2)

# Depth Type
matrix = add_var(matrix, var="DEPTH_TYPE", const='CONST', value='DATA')

# Spatial Coordinates
matrix = add_var(matrix, var="Mglob", const='CONST', value=586)
matrix = add_var(matrix, var="Nglob", const='CONST', value=3)

# Time
matrix = add_var(matrix, var="TOTAL_TIME", const='CONST', value=400.0)
matrix = add_var(matrix, var="PLOT_INTV", const='CONST', value=0.05)
matrix = add_var(matrix, var="PLOT_INTV_STATION", const='CONST', value=0.5)
matrix = add_var(matrix, var="SCREEN_INTV", const='CONST', value=100.0)
matrix = add_var(matrix, var="PLOT_START_TIME", const='CONST', value=0.0)

# Grid size
matrix = add_var(matrix, var="DX", const='CONST', value=0.27466501965706874)
matrix = add_var(matrix, var="DY", const='CONST', value=0.27466501965706874)

# Wavemaker
matrix = add_var(matrix, var="WAVEMAKER", const='CONST', value='WK_REG')
matrix = add_var(matrix, var="DEP_WK", const='CONST', value=1.9373709971858077)
matrix = add_var(matrix, var="Xc_WK", const='CONST', value=50.420636740210035)
matrix = add_var(matrix, var="Yc_WK", const='CONST', value=0.0)
matrix = add_var(matrix, var="Tperiod", const='CONST', value=6.0)
matrix = add_var(matrix, var="AMP_WK", const='CONST', value=0.2)
matrix = add_var(matrix, var="Theta_WK", const='CONST', value=0.0)
matrix = add_var(matrix, var="Delta_WK", const='CONST', value=3.0)

# Boundary Conditions
matrix = add_var(matrix, var="PERIODIC", const='CONST', value='F')

# Sponge layer
matrix = add_var(matrix, var="DIFFUSION_SPONGE", const='CONST', value='F')
matrix = add_var(matrix, var="FRICTION_SPONGE", const='CONST', value='T')
matrix = add_var(matrix, var="DIRECT_SPONGE", const='CONST', value='T')
matrix = add_var(matrix, var="Csp", const='CONST', value=0.0)
matrix = add_var(matrix, var="CDsponge", const='CONST', value=1.0)
matrix = add_var(matrix, var="Sponge_west_width", const='CONST', value=25.210318370105018)
matrix = add_var(matrix, var="Sponge_east_width", const='CONST', value=0.0)
matrix = add_var(matrix, var="Sponge_south_width", const='CONST', value=0.0)
matrix = add_var(matrix, var="Sponge_north_width", const='CONST', value=0.0)

# Numerics
matrix = add_var(matrix, var="Cd", const='CONST', value=0.0)
matrix = add_var(matrix, var="CFL", const='CONST', value=0.5)
matrix = add_var(matrix, var="FroudeCap", const='CONST', value=3.0)

# Wet-Dry
matrix = add_var(matrix, var="MinDepth", const='CONST', value=0.01)

# Wave Breaking
matrix = add_var(matrix, var="VISCOSITY_BREAKING", const='CONST', value='T')
matrix = add_var(matrix, var="Cbrk1", const='CONST', value=0.65)
matrix = add_var(matrix, var="Cbrk2", const='CONST', value=0.35)

# Steady Time
matrix = add_var(matrix, var="T_INTV_mean", const='CONST', value=20.0)
matrix = add_var(matrix, var="STEADY_TIME", const='CONST', value=20.0)

# Output Variables
matrix = add_var(matrix, var="DEPTH_OUT", const='CONST', value='T')
matrix = add_var(matrix, var="FIELD_IO_TYPE", const='CONST', value='BINARY')
matrix = add_var(matrix, var="ETA", const='CONST', value='T')
matrix = add_var(matrix, var="MASK", const='CONST', value='T')
matrix = add_var(matrix, var="WaveHeight", const='CONST', value='T')


# %%

