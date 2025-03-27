import matplotlib.pyplot as plt
import numpy as np
import os

def plot_spectra(var_dict):
    # Unpack -----------------------------------------------------------------
    tri = var_dict['D3_Trial']
    WK = var_dict['WK']
    ITER = var_dict['ITER']
    T_lower = var_dict['T_lower']
    T_higher = var_dict['T_higher']
    # Unpack -----------------------------------------------------------------
    
    T = WK.period.values
    amp  = WK.amp.values
    Peak_period = WK.PeakPeriod
    T_ind = np.argmin(np.abs(T-Peak_period))
    
    fig,ax = plt.subplots(dpi=200)
    ax.plot(T,amp)
    ax.grid(True)
    ax.set_xlabel('Period (s)')
    ax.set_ylabel('Amplitude of Wave Component (m)')
    ax.set_title(f'Trial {tri}: Lower Bound {T_lower}, Upper Bound {T_higher}')
    ax.scatter(T[T_ind],amp[T_ind],color='red',label=f'Peak Period = {Peak_period:.2f}',zorder=5)
    ax.legend()
    fig.tight_layout()
    file_base = os.getenv('sp_fig')
    file_name = f'spectra_fig_{ITER:05}.png'
    file_path = os.path.join(file_base,file_name)
    fig.savefig(file_path)
    
    plt.close(fig)
    
    return