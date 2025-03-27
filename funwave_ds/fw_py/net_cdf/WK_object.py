import xarray as xr
import numpy as np
class WK_TIME_SERIES(xr.Dataset):
    __slots__ = ()

    ## INITIALIZE =========================================================
    def __init__(self, period=None,
                       amp=None,
                       phase=None,
                       PeakPeriod = None):

      # Initialize the xarray Dataset with coordinates
      super().__init__(coords={'period': period})

      # Store important spatial parameters as attributes
      self['amp'] = (('period'), amp)  
      self['phase'] = (('period'), phase)  

      # Store important spatial parameters as attributes
      self.attrs['NumWaveComp']  = len(period)

      if PeakPeriod is None:
         i_peak = np.argmax(amp)
         self.attrs['PeakPeriod'] = period[i_peak]
         

    ## [END] INITIALIZE =========================================================


    ## STATIC METHOD
    @staticmethod
    def get_fft_values(t=None,
                       eta=None,
                       f_lo=None,
                       f_hi=None):
      t = t.flatten()
      eta = eta.flatten()
      # Assert time and series the same length
      assert(len(t)==len(eta)),'t and eta must have the same length!'
      
      # Basic Info
      dt = t[1]-t[0]     # time step
      N = len(eta)       # record length
      
      # FFT and associated frequencies
      fft_values = np.fft.fft(eta) 
      f = np.fft.fftfreq(N, d=dt)

      # Cut to Nyquist
      f = f[:N//2]
      fft_values = fft_values[:N//2]

      # Amplitude and Phase at each frequency
      amp = 2*np.abs(fft_values) /N
      phase = -np.angle(fft_values)

      # Cut off if necessary
      if f_lo:
         f,amp,phase = f[f>f_lo],amp[f>f_lo] , phase[f>f_lo]
      if f_hi:
         f,amp,phase = f[f<f_hi],amp[f<f_hi] , phase[f<f_hi]
      
      return f,amp,phase