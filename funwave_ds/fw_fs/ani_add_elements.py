import matplotlib.pyplot as plt
import numpy as np
import cv2
'''
This file has functions needed to add elements and animate relevant variables
in an animation
'''

#%% ADD ELEMENTS
'''
This section deals with adding elements to an animation that have already 
been set up
'''
def add_static_variables(variables, static_variables, animation_variables):
    
    fig = animation_variables['fig']
    ax = animation_variables['ax']
    for attr in static_variables:
        print(f'adding {attr}')
        key = attr['key']
        color = attr.get('color', 'black')
        linestyle = attr.get('linestyle', '--')
        linewidth = attr.get('linewidth', 2)
        label = attr.get('label', key)

        if key in variables:
            ax.axvline(x=float(variables[key]), color=color, linestyle=linestyle, linewidth=linewidth, label=label)
        else:
            print(f"Warning: No position ({key}) found.")
            
    add = {'ax': ax,
           'fig': fig}
    ani_ = {**animation_variables, **add}
    
    return animation_variables


def add_dynamic_variables_0(variables, dynamic_variables, animation_variables):
    fig = animation_variables['fig']
    ax = animation_variables['ax']
    
    if not 'mask' in variables:
        print('Warning: No mask found.')
        
    lines = []
    out_variables = []
    for var in dynamic_variables:
        # Get variable and its relevant coordinate
        key = var['key']
        coord = variables[var['coord']]
        
        # Squeeze to 1D, apply mask if present
        outvar = np.squeeze(variables[key][:,1,:])
        if 'mask' in variables:
            mask = np.squeeze(variables['mask'][:,1,:])
            outvar[mask == 0] = np.nan
            
        
        # Get aesthetics
        color = var.get('color', 'black')
        linestyle = var.get('linestyle', '-')
        linewidth = var.get('linewidth', 2)
        label = var.get('label', key)

        if key in variables:
            print(key)
            line, = ax.plot(coord, outvar[0,:], color=color, linestyle=linestyle, linewidth=linewidth, label=label)
            lines.append(line)  # Store line object
            out_variables.append(outvar)
            #ax.axvline(x=v_[key], color=color, linestyle=linestyle, linewidth=linewidth, label=label)
        else:
            print(f"Warning: No position ({key}) found.")
            
    add = {'lines': lines,
           'out_variables': out_variables}
    ani_ = {**animation_variables, **add}
    return ani_


def add_legends_labels(variables, attribute_labels, animation_variables):
    fig = animation_variables['fig']
    ax = animation_variables['ax']
    
    plt.title(animation_variables['title_string'])
    plt.xlabel('Cross Shore position (m)')
    plt.ylabel(animation_variables['ylabel'])
    minima = np.min(-np.squeeze(variables['Z'][:,1]))
    plt.ylim(minima, 2)
    plt.grid(True)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), frameon=True, ncol=2)
    fig.tight_layout()  
    fig.tight_layout() 
    

    return animation_variables


def animate_dynamic_variables(variables, dynamic_variables, animation_variables):
    fig = animation_variables['fig']
    ax = animation_variables['ax']
    time_counter = animation_variables['time_counter']
    lines = animation_variables['lines']
    out_variables = animation_variables['out_variables']
    
    # Loop through all timesteps
    for t_i in range(0, len(variables['t_FW']), animation_variables['stride']):
       
        print(f'\t\t\tplotting up to time {variables["t_FW"][t_i]}')
        
        # Update time counter box
        animation_variables['time_counter'].set_text(f'time = {variables["t_FW"][t_i]:.2f}')  # Change the text content
    
        
        # Update time-step variables
        for line, outvar in zip(lines, out_variables):
            line.set_ydata(outvar[t_i,:])
            
            # Update movie
            fig.canvas.draw()
            width, height = fig.canvas.get_width_height()       # Plot dimensions
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape((height, width, 3))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  
            animation_variables['out'].write(image)
    
    # Finish the animation
    animation_variables['out'].release()
    print(f"\t\t Finished Animation!")
    return animation_variables