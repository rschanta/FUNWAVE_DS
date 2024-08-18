# dep_flat_reg

## Description
**dep_flat_reg** contains FUNWAVE simulation runs for the DEP_TYPE=SLOPE regime of FUNWAVE for the regular wavemaker on a 1D (Nglob = 3)beach profile


## Design Matrices
### Design Matrix 1: 
Design matrix 1 uses the following ranges of model parameters:
#### Ranged Parameters:
| Parameter | Lower Bound| Upper Bound | Number of Points
|---|---|---|---|
|**SLP** | 0.01 | 0.1 | 10 |
| **Tperiod** | 4 | 14 | 11 |
| **AMP_WK** | 0.2 | 0.6 | 9 | 
| **DEPTH_FLAT** | 2 | 10 | 9 | 
#### List Parameters:
*There are no list parameters for this matrix*
#### Notable Constant Parameters
| Parameter | Value | Significance |
|---|---|---|
|**GAMMA_BEACH** | 0.75 | Portion of profile above the still MWL on the east| 
|**CHI_Xslp** | 5 | Xslp = (CHI_Xslp)*(Wavelength)|
|**OMEGA_WK** | 2.25 | Xc_WK = (OMEGA_WK)*(Wavelength)|
|**SIGMA_SP**| 1.25 | Sponge_west_width = (SIGMA_SP)*(Wavelength)|
|**PLOT_INTV**| 0.05 | Reasonable computational time|
|**TOTAL_TIME**| 300.0 | Reasonable computational time|

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