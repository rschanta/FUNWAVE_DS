import matplotlib.pyplot as plt
import numpy as np
import cv2


'''
This file contains the functions needed to set up an animation from a FUNWAVE
output from a netcdf file

    `set_up_animation` sets up the basic geometry of the plot
    `set_up_movie_writer` deals with the objects required for movie writing
    `get_stride` does some of the math to determine a good frame rate/stride
'''


def get_stride(variables,animation_variables):
    coarseness = animation_variables['coarseness']
    speed = animation_variables['speed']
    dt_av = np.mean(variables['t_FW'][1:]-variables['t_FW'][0:-1]) # Use average dt to inform stride
    
    #speed = 1                       # model time displayed in 1 second of animation time                  
    #coarseness = 0.5                 # model time between each frame in the animation
    fr = float(speed)/float(coarseness)            # required frame rate for this to work
    stride = int(float(coarseness)/dt_av)+1   # space between indices for this to work
    
    add = {'fr': fr,
            'stride': stride}
    ani_ = {**animation_variables, **add}
    return ani_


def set_up_animation(variables,animation_variables,plot_bathy=True):
    
    # Basic figure setup
    fig, ax = plt.subplots(figsize=(6, 4), dpi=200)     # Set size and resolution
    width, height = fig.canvas.get_width_height()       # Plot dimensions
    
    if plot_bathy:
        X = variables['X']
        Z = -np.squeeze(variables['Z'][:,1])
        bathy_line, = ax.plot(X, Z, lw=2, color = 'black')
    
    # Time counter
    time_counter = ax.text(0.05, 0.95, 'time = 0.00',
                   transform=ax.transAxes,  # Use relative coordinates
                   fontsize=12,
                   verticalalignment='top',
                   horizontalalignment='left',
                   bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    
    # Other animation components
    
    add = {'width': width,
            'height': height,
            'fig': fig,
            'ax': ax,
            'time_counter': time_counter}
    ani_ = {**animation_variables, **add}

    return fig,ax,ani_


def set_up_movie_writer(variables,
                        animation_variables):
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')   # '*XVID' = .avi file
    path = animation_variables['path']
    print(f'The Path is {path}')
    fr = animation_variables['fr']
    width = animation_variables['width']
    height = animation_variables['height']
    out = cv2.VideoWriter(path, fourcc, fr, (width, height))
    
    add = {'out': out}
    animation_variables = {**animation_variables, **add}
    
    return animation_variables