# dep_flat_reg

## Description
**dep_flat_reg** contains FUNWAVE simulation runs for the DEP_TYPE=SLOPE regime of FUNWAVE for the irregular (TMA) wavemaker on a 1D (Nglob = 3)beach profile


## Design Matrices
### Exploratory_1: 
Exploratory_1 is the first attempt to explore this parameter space a bit.
#### Ranged Parameters:
| Parameter | Lower Bound| Upper Bound | Number of Points
|---|---|---|---|
|**SLP** | 0.04 | 0.08 | 3 |
|**FreqPeak** | 0.075 | 0.2 | 4 |
| **Hmo** | 0.4 | 1.0 | 4 | 

#### List Parameters:
*There are no list parameters for this matrix*

#### Notable Constant Parameters
| Parameter | Value | Significance |
|---|---|---|
|**FreqMin** | 0.05 | Period = 20 s|
|**FreqMax** | 0.3 | Period = 3.33 s|
|**GammaTMA**| 3.3 | Default (eq. to JONSWAP)|
|**GAMMA_BEACH** | 0.75 | Portion of profile below the still MWL on the west| 
|**SIGMA_SP**| 1.25 | Sponge_west_width = (SIGMA_SP)*(Wavelength)|
|**PLOT_INTV**| 0.05 | Reasonable computational time|
|**TOTAL_TIME**| 300.0 | Reasonable computational time|
| **DEPTH_FLAT** | 3 | Shallow Water|

#### Dependent Parameters
| Parameter | Function | Dependencies | Rationale | 
|---|---|---|---|
| **L_** | `stability_vars_1()`   | Tperiod, DEPTH_FLAT | representative wavelength |
| **DX** | `stability_vars_1()`   | L_, DEPTH_FLAT | Torres 2022 stability criteria |
| **DY** | `stability_vars_1()` | DX | = DX | 
| **DEP_WK** | `stability_vars_1()` | DEPTH_FLAT | = DEPTH_FLAT | 
| **Sponge_width_west** | `stability_vars_1()` | L_, SIGMA_SP  | Torres 2022 stability criteria | 
| **Xc_WK** | `stability_vars_1()` | L_, OMEGA_WK | Torres 2022 stability criteria | 
|**Xslp** | `beach_geometry_1()` | L_, GAMMA_BEACH| Ensure enough flat room for wave propagation|
|**Mglob** | `beach_geometry_1()` | Mglob, DX, DEPTH_FLAT, SLP, gamma_beach| Ensure geometry is possible for DX |