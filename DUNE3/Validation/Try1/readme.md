# Try 1

## Description
This is a first naïve attempt to validate FUNWAVE-TVD on the data. The general idea is to use the *incident* waveform $\eta_i$ from the filetered dataset to act as forcing at the wavemaker specified by `WK_TIME_SERIES`

## Additional Parameters
The following parameters are used in this experimental run:

### Static
| **Parameter Name** | **Parameter**| Significance |Value |
|--|--|--|--|
| $\pi_2$ | `PI_2` | Distance of `Xc_WK` in terms of wavelengths | 3 |
| $\pi_3$ | `PI_3` | Distance of `Sponge_west_width` in terms of wavelengths | 1.5 |
| $\pi_4$ | `PI_4` | "Buffer" distance between the western wavemaker and the edge of the model domain to ensure local flatness (should be small, <<1)| 0.1 |
| $T_{min}$ | `lo` | lowest period to keep in the FFT of $\eta_i$| 1.5 |
| $T_{hi}$ | `hi` | highest period to keep in the FFT of $\eta_i$| 20 |

The $\pi$ parameters are largely just for stability and shouldn't have a major impact on the numerical solution for reasonable values. What may be interesting is the values of $T_{min}$ and $T_{max}$, since the range spanned by these values correspond to the domain of the frequency space. Up to 20 as an infragravity band is the starting point.

### Ranged
The main goal is to just loop over every trial:
| **Parameter Name** | **Parameter**| Significance | Range |
|--|--|--|--|
| Dune 3 Trial | `D3_trial` | Dune 3 Trial | (5,24,20)



## Dependent Parameters
One standard pipeline is used for this process:

```python
function_sets = {'Standard' : [mod.get_spectra,
                               mod.set_spectra,
                               mod.get_bathy,
                               mod.get_hydro,
                               mod.set_bathy]}
```
###  1: Get FFT of the time series (`get_spectra`)
[[CODE](./model_code/spectra.py)] This function extracts the time series of the incident wave $\eta_i$ as used by Tsai in his wavemaker in OpenFOAM.

- Cuts the time series $\eta_i$ between `t0` and `t_end`
- Takes the FFT of $\eta_i$ using `np.fft.fft`, returning an imaginary number for each of $j$ frequencies:

$$X_j = a_j + b_ji = \mathcal{F}(\eta_i)$$

- Constructs the frequency axis for this tranform 
- Cuts both frequency and FFT transform to the Nyquist frequency range
- Calculate the amplidue at each frequency:
$$a_0 = |X_j|$$
- Calculate the phase of each frequency (note that his is the `np.angle` function with a negative to respect quadrant conventions):
$$\phi_j=-\arctan{\frac{b_j}{a_j}}$$

### 2: Filter Incident Waves (`set_spectra`)
[[CODE](./model_code/spectra.py)] Crudely, without more advanced spectral filtering, frequencies are just removed to ensure all periods are between $T_{min}$ and $T_{max}$

### 3: Get the bathymetry data (`get_bathy`)
[[CODE](./model_code/bathy.py)] Three arrays are extracted from the data:
- The X positions of the batymetry points in the tank from the filtered dataset
- The Z positions of the bathymetry in the tank from the filtered dataset (recall this is actually measured from the bottom)
- The MWL in the raw dataset, assumed to be at the quiscient surface.

### 4: Finding a Representative Wavelength (`get_hydro`)
The linear dispersion relation is solved using the PeakPeriod identified in the spectral analysis and a water depth given by `MWL[0]-Z[0]` since the wavemaker is on the left hand side.

### 5: Setting up the domain (`set_bathy`)
The domain is dynamically set using the $\pi$ parameters and Torres stability criteria:

## Additional Files Created
### Plots
- Bathymetry Diagrams
- Spectra Diagrams 

### Input Files
- DEP_FILE
- WAVE_COMP_FILE