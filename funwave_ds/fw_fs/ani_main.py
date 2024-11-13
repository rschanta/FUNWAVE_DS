
"""
This is the main function to be called to invoke animation
"""

from .ani_add_elements import *
from .ani_setup import *
from .ani_unpack import *

def create_animation(ds,
                     static_variables,
                     dynamic_variables,
                     attribute_labels,
                     animation_variables):
    
    # Extract the variables from the netcdf
    
    
    variables = extract_variables_out(ds,static_variables,dynamic_variables,attribute_labels)
    
    # Set up the animation
    fig,ax,animation_variables = set_up_animation(variables,
                                                  animation_variables,
                                                  plot_bathy=True)
    
    # Time: Determine the frame rate and stride
    animation_variables = get_stride(variables,
                                     animation_variables)
    
    # Set up the movie writer
    animation_variables = set_up_movie_writer(variables,
                                              animation_variables)
    
    # Add the static variables
    animation_variables = add_static_variables(variables, 
                                               static_variables, 
                                               animation_variables)
    
    # Add the dynamic variables: first step
    animation_variables = add_dynamic_variables_0(variables, 
                                                  dynamic_variables, 
                                                  animation_variables)   
    
    # Add the legends, labels, and formatting
    animation_variables = add_legends_labels(variables, 
                                             attribute_labels,
                                             animation_variables) 
    
    
    # Step through time for the dynamic variables
    animation_variables = animate_dynamic_variables(variables, 
                                                    dynamic_variables,
                                                    animation_variables)  
    
    return animation_variables
        