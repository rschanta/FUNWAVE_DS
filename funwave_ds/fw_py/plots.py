import numpy as np
import matplotlib.pyplot as plt

# TODO Also make a bit moe general, yknow?
def plot_bathy(dicta,ptr):
    # Pull out params
    X = dicta['files']['bathy']['array'][:,0]
    Z = -dicta['files']['bathy']['array'][:,1]
    Xc_WK = dicta['Xc_WK']
    DX = dicta['DX']
    DY = dicta['DY']
    Mglob = dicta['Mglob']
    Nglob = dicta['Nglob']
    
        
    
    plt.plot(X,Z,label='Bathymetry',color='black')
    # Add wavemaker
    if 'WAVEMAKER' in dicta:
        plt.axvline(x=Xc_WK, color='red', linestyle='--', label='Wavemaker')
    # Check sponge
    count = 0
    for key in ['DIRECT_SPONGE','FRICTION_SPONGE','DIFFUSION_SPONGE']:
            if key in dicta and dicta[key] == 'T' and count ==0:
                Sponge_W = dicta['Sponge_west_width']
                Sponge_E = dicta['Sponge_east_width']
                if Sponge_W != 0:
                    plt.axvline(x=Sponge_W, color='darkgreen', linestyle='--', label='West Sponge')
                if Sponge_E != 0:
                    plt.axvline(x=Sponge_E, color='lightgreen', linestyle='--', label='East Sponge')
                count = count + 1
    # Check if the key exists
    if 'ALT_TITLE' in dicta:
        plt.title('INPUT BATHYMETRY: ' + dicta['ALT_TITLE'] + '\n' + dicta['TITLE'] )
    else:
        plt.title('INPUT BATHYMETRY: ' +  dicta['TITLE'])
        
    plt.text(1.05, 0.5, f'DX = {DX:.2f} DY = {DY:.2f}\nMglob = {Mglob} Nglob = {Nglob}', 
             fontsize=12, 
             bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'),
             transform=plt.gca().transAxes,
             verticalalignment='center')
    
    # Adjust the plot's x and y limits to make space for the textbox
    #plt.xlim(x.min(), x.max() + 2)
    plt.grid()
    plt.xlabel('Cross-shore Position (x)')
    plt.ylabel('Depth (z)')
    plt.legend()
    plt.savefig(ptr['b_fig'], dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    return

def plot_bathy2(var_dict,ptr):
    # Pull out params
    X = var_dict['bathy'][:,0]
    Z = -var_dict['bathy'][:,1]
    Xc_WK = var_dict['Xc_WK']
    DX = var_dict['DX']
    DY = var_dict['DY']
    Mglob = var_dict['Mglob']
    Nglob = var_dict['Nglob']
        
    
    plt.plot(X,Z,label='Bathymetry',color='black')
    # Add wavemaker
    if 'WAVEMAKER' in var_dict:
        plt.axvline(x=Xc_WK, color='red', linestyle='--', label='Wavemaker')
    # Check sponge
    count = 0
    for key in ['DIRECT_SPONGE','FRICTION_SPONGE','DIFFUSION_SPONGE']:
            if key in var_dict and var_dict[key] == 'T' and count ==0:
                Sponge_W = var_dict['Sponge_west_width']
                Sponge_E = var_dict['Sponge_east_width']
                if Sponge_W != 0:
                    plt.axvline(x=Sponge_W, color='darkgreen', linestyle='--', label='West Sponge')
                if Sponge_E != 0:
                    plt.axvline(x=Sponge_E, color='lightgreen', linestyle='--', label='East Sponge')
                count = count + 1
    # Check if the key exists
    if 'ALT_TITLE' in var_dict:
        plt.title('INPUT BATHYMETRY: ' + var_dict['ALT_TITLE'] + '\n' + var_dict['TITLE'] )
    else:
        plt.title('INPUT BATHYMETRY: ' +  var_dict['TITLE'])
        
    plt.text(1.05, 0.5, f'DX = {DX:.2f} DY = {DY:.2f}\nMglob = {Mglob} Nglob = {Nglob}', 
             fontsize=12, 
             bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'),
             transform=plt.gca().transAxes,
             verticalalignment='center')
    
    # Adjust the plot's x and y limits to make space for the textbox
    #plt.xlim(x.min(), x.max() + 2)
    plt.grid()
    plt.xlabel('Cross-shore Position (x)')
    plt.ylabel('Depth (z)')
    plt.legend()
    plt.savefig(ptr['b_fig'], dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    return

def plot_TS_spectra(dicta,ptr):
    # Pull out params
    period = dicta['files']['spectra']['per']
    amp = dicta['files']['spectra']['cnn']
    peak = dicta['files']['spectra']['peak_per']
    num_comp = dicta['files']['spectra']['num_components']
    # Check if the key exists
    if 'ALT_TITLE' in dicta:
        plt.title('INPUT SPECTRA: ' + dicta['ALT_TITLE'] + '\n' + dicta['TITLE'] )
    else:
        plt.title('INPUT SPECTRA: ' + dicta['TITLE'])
    plt.plot(period,amp)
    
    plt.text(1.05, 0.5, f'Peak Period = {peak:.2f}\n Components = {num_comp}', 
             fontsize=12, 
             bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'),
             transform=plt.gca().transAxes,
             verticalalignment='center')
    plt.grid()
    plt.xlabel('Period (s)')
    plt.ylabel('Magnitude')
    plt.savefig(ptr['sp_fig'], dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    return


def plot_TS_spectra2(dicta,ptr):
    # Unpack variables
    per = vars['spectra']['per']
    enn = vars['spectra']['enn']
    cnn = vars['spectra']['cnn']
    ITER = vars['ITER']
    super_path = vars['super_path']
    run_name = vars['run_name']
    
    print('Started plotting Spectra...')

    fpy.make_FW_paths(super_path, run_name)
    p = fpy.get_FW_paths(super_path, run_name)
    ptr = fpy.get_FW_tri_paths(ITER, p)

    # Save to file
    plt.plot(per,enn)
    plt.grid()
    plt.xlabel('Period (s)')
    plt.ylabel('Amplitude')
    plt.show()
    plt.savefig(ptr['sp_fig'], dpi=300, bbox_inches='tight')
    plt.close()
    print(f'Spectra file successfully saved to: {ptr["sp_fig"]}')
    
    return {}