# Dune3

## Description
**Dune3** contains FUNWAVE simulation runs for Dune3


## Design Matrices
### Validate_1: 
Validate_1 is the first attempt to explore this parameter space a bit.
#### Ranged Parameters:
| Parameter | Lower Bound| Upper Bound | Number of Points | Significance
|---|---|---|---|---|
|**D3_trial** | 5 | 24 | 20 | Which trial of Dune3 Dataset to use | 

#### List Parameters:
*There are no list parameters for this matrix*

#### Notable Constant Parameters
| Parameter | Value | Significance |
|---|---|---|
|**lo** | 0.05 | Period = 20 s|
|**hi** | 0.3 | Period = 3.33 s|
|**WG_to_use**| 3.3 | Default (eq. to JONSWAP)|
|**PLOT_INTV**| 0.05 | Reasonable computational time|


#### Dependent Parameters
| Parameter | Function | Dependencies | Rationale | 
|---|---|---|---|
| **pickle_file** | `get_pickle_path()`   | D3_trial, DATA_DIR | pickle file for the data associated with D3Trial |
| **spectra** | `get_spectra()`   | lo, hi, WG_to_use, pickle_file | Gets the FFT, time series spectra |
| **DY** | `stability_vars_1()` | DX | = DX | 
| **DEP_WK** | `stability_vars_1()` | DEPTH_FLAT | = DEPTH_FLAT | 
| **Sponge_width_west** | `stability_vars_1()` | L_, SIGMA_SP  | Torres 2022 stability criteria | 
| **Xc_WK** | `stability_vars_1()` | L_, OMEGA_WK | Torres 2022 stability criteria | 
|**Xslp** | `beach_geometry_1()` | L_, GAMMA_BEACH| Ensure enough flat room for wave propagation|
|**Mglob** | `beach_geometry_1()` | Mglob, DX, DEPTH_FLAT, SLP, gamma_beach| Ensure geometry is possible for DX |