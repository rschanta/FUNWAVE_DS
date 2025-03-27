import scipy.signal as sig 
import numpy as np
import xarray as xr


def clean_and_interpolate(ds):
    '''
    For the time and eta output at the station files, this function removes
    any duplicate time steps (artifact of how FUNWAVE outputs station data)
    and interpolates it to a uniform timestep based on PLOT_INTV_STATION. The
    end result is an xarray ready for Fourier Analysis
    '''
    # Unpack values
    t_FW = ds['t_station'].values
    GAGE_NUM = ds['GAGE_NUM'].values
    eta = ds['eta_sta'].values
    plot_intv_station = ds.attrs['PLOT_INTV_STATION']
    
    # Find unique values and their indices, sort
    t_FW_unique, unique_t_FW_indices = np.unique(t_FW, return_index=True)
    sorted_indices = np.sort(unique_t_FW_indices)
    
    # Retain only these
    t_clean = t_FW[sorted_indices]
    eta_clean = eta[:,sorted_indices]
    
    # Grid of times to interpolate to
    t_interp = np.arange(0,t_clean[-1],plot_intv_station)
    
    # Initialize array for interpolated eta
    eta_interp = np.zeros((eta_clean.shape[0],len(t_interp) ))
    
    # Loop through each column (station) to interpolate
    for i in range(eta_clean.shape[0]):
        foo = np.interp(t_interp, t_clean, eta_clean[i,:])
        eta_interp[i,:] = foo
    
    # Add to array
    eta_interp = xr.DataArray(
    eta_interp,
    dims=("GAGE_NUM", "t_clean"),
    coords={"t_clean": t_interp, "GAGE_NUM": GAGE_NUM},
    name="eta"
    )
    
    ds["eta_clean"] = eta_interp
    return ds

def calculate_spectra(ds,tau):
    
    # Unpack ------------------------------------------------------------------
    PLOT_INTV_STATION = ds.attrs['PLOT_INTV_STATION']
    t = ds['t_clean'].values
    eta = ds["eta_clean"].values
    GAGE_NUM = ds['GAGE_NUM'].values
    Tperiod = ds.attrs['Tperiod']
    # ------------------------------------------------------------------------
    
    # Count back how many periods to use and index
    t_start = t[-1] - tau*Tperiod 
    eta_cut = eta[:,t > t_start]
    
    # Time Series Values
    fs = 1/PLOT_INTV_STATION

    # Get dimensionality
    N_len = eta_cut.shape[0] 
    t_len = eta_cut.shape[1] 
    
    
    # Given time window size
    twindow = t_len

    # Define window lengths
    fft_windows = [2048,1024,512,256,128,64]
    # Find the largest window that will fit within the data
    for i, fwin in enumerate(fft_windows):
        if twindow > fwin:
            nFFT = fft_windows[i]
            break  
    
    # Specify 50% overlap
    nOverlap = nFFT / 2 
    
    # Length of frequency axis
    f_len = nFFT // 2 + 1
    
    # Construct a window
    myWindow=np.bartlett(nFFT)
    
    
    # Initialize things
    spec_array = np.zeros((N_len,f_len))
    Etot,Hrms,Hmo,Tpeak,Epeak = [],[],[],[],[]

    
    for k in range(N_len):
        
        # Slice out the station
        eta_slice = eta_cut[k,:]
    
        # Calculate power spectral density at this station
        f, Pxx_spec_den = sig.welch(x=eta_slice, 
                                    fs=fs,             
                                    window=myWindow,     
                                    nperseg=nFFT,      
                                    noverlap=nOverlap, 
                                    nfft=nFFT,         
                                    scaling='density')      
        
        # Calculate width of frequency bin
        dfreq = fs / nFFT
        
        # Calculate the energy
        Etot_=np.sum(Pxx_spec_den*dfreq)
        
        # Calculate significant wave heights
        Hrms_=np.sqrt(Etot_*8)
        Hmo_ = np.sqrt(2.0) * Hrms_   
        
        # Calculate peak
        pk = np.where(Pxx_spec_den == max(Pxx_spec_den))[0][0]
        Epeak_ = np.sum(Pxx_spec_den*dfreq)
        Tpeak_ = 1/f[pk]
        
        # Append to arrays
        Etot.append(Etot_)
        Hrms.append(Hrms_)
        Hmo.append(Hmo_)
        Tpeak.append(Tpeak_)
        Epeak.append(Epeak_)
        
        # Add to array
        spec_array[k,:] = Pxx_spec_den

            
    # Create normalized energy
    Enorm = Etot/np.max(Etot)
    
    
    # Add spectrum to array
    spec_array = xr.DataArray(
        spec_array, dims=("GAGE_NUM", "f"),
        coords={"f": f, "GAGE_NUM": GAGE_NUM}, name="spec_array")
    
    # Add to dataset
    Etot = xr.DataArray(Etot, dims="GAGE_NUM", coords={"GAGE_NUM": GAGE_NUM}, name="Etot")
    Enorm = xr.DataArray(Enorm, dims="GAGE_NUM", coords={"GAGE_NUM": GAGE_NUM}, name="Enorm")
    Hrms = xr.DataArray(Hrms, dims="GAGE_NUM", coords={"GAGE_NUM": GAGE_NUM}, name="Hrms")
    Hmo = xr.DataArray(Hmo, dims="GAGE_NUM", coords={"GAGE_NUM": GAGE_NUM}, name="Hmo")
    Tpeak = xr.DataArray(Tpeak, dims="GAGE_NUM", coords={"GAGE_NUM": GAGE_NUM}, name="Tpeak")
    Epeak = xr.DataArray(Epeak, dims="GAGE_NUM", coords={"GAGE_NUM": GAGE_NUM}, name="Epeak")

    
    
    # Add to dataset
    ds["Sxx"] = spec_array
    ds["Etot"] = Etot
    ds["Enorm"] = Enorm
    ds["Hrms"] = Hrms
    ds["Hmo"] = Hmo
    ds["Tpeak"] = Tpeak
    ds["Epeak"] = Epeak
    
    # Subset just the things added, keep attributes though
    ds = ds[["Sxx", "Etot","Enorm","Hrms","Hmo","Tpeak","Epeak"]]
    return ds



def compress_all_outputs(datasets):
    # List of datasets created
    stacked_datasets = []
    
    # Loop through all datasets
    for i, dataset in enumerate(datasets):
        print(f'\tWorking on dataset number {i}',flush=True)
        ds = xr.load_dataset(dataset)
        # Add a new dimension: ITER
        ds_expanded = ds.expand_dims(dim={"ITER": [i]})
        
        # Expand attributes along ITER
        for key,value in ds.attrs.items():
            # Wrap scalar or string into a 1-element list
            ds_expanded[key] = xr.DataArray([value], dims="ITER")
        
        # Add the dataset to the list
        stacked_datasets.append(ds_expanded)
        print(f'\t\tFinished dataset number {i}',flush=True)

    print('Finished Loop',flush=True)
    # Concatenate along ITER
    stacked_ds = xr.concat(stacked_datasets, dim="ITER")
    # Remove redundant attributes
    stacked_ds.attrs = {}
    print('Finished Function!',flush=True)
    return stacked_ds



