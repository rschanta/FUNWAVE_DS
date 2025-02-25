# DX_Sens: Sensitivity Analysis of `DX` 

## Description
This is a sensitivity analysis on `DX`, assessing the affect of varying it within the range identified as stable by Torres (2022).

## Definition of Key Parameters
The following parameters are used in this experimental run, as specified in [`DX_Sens.csv`](./design_matrices/DX_Sens.csv).

### Static Parameters
| **Parameter Name** | **Parameter**| Significance |Value |
|--|--|--|--|
| $\pi_1$ | `PI_1` | See [general documentation](../readme.md) | 4 |
| $\pi_2$ | `PI_2` | See [general documentation](../readme.md) | 1 |
| $\pi_3$ | `PI_3` | See [general documentation](../readme.md)| 50 |
| $\pi_4$ | `PI_4` | See [general documentation](../readme.md)| 100 |
| $\pi_5$ | `PI_5` | See [general documentation](../readme.md)| 4 |
| $\tau_1$ | `TAU_1` | See [general documentation](../readme.md)| 150 |
| $\xi_1$ | `XI_1` | See [general documentation](../readme.md)| 0.05 |

These are all consistent with with the standard setup in the `FLAT_TANK` runs, corresponding to very linear waves ($\epsilon = 0.05$) over 150 wave periods.

### Ranged
Here, we dynamically range over typical periods/depths for shallow water depths in the ordinary gravity wave range, which would be standard wind-driven waves not in the capillary/infragravity bands:
| **Parameter Name** | **Parameter**| Significance | Range |
|--|--|--|--|
| Period | `Tperiod` | Ordinary gravity wave range | (2,16,15)
| Water Depth | `DEPTH_FLAT` | Standard shallow water depths | (1,20,20)

### List Parameters
The only list parameter is $\pi_6$, which corresponds to where in the range of stable `DX` values we are. Recall that the stable range for `DX` identified by Torres is:

$$ \frac{h}{15}  < \texttt{DX} < \frac{\lambda_0}{60}$$

So the value of `DX` is set by:

$$ \frac{h}{15} + \pi_6 \left(\frac{\lambda_0}{60} - \frac{h}{15} \right)$$

where $\pi_6$ can range from 0 (lower bound) to 1 (upper bound). The following values are used:
| **Parameter Name** | **Parameter**| Significance |Values |
|--|--|--|--|
| $\pi_6$ | `PI_6` | Position in the stable range of `DX`| 0.15,  0.5, 0.85 |

effectively testing 3 `DX` choices at the lower, middle, and upper ends of the stable range


### Dependent Parameters
The following parameters are calculated dynamically for each run to meet the constraints set by the problem:

|  **Parameter**| Pipeline Function|
|--|--|
| `Sponge_west_width` | `set_domain()` | 
| `Xc_WK` | `set_domain()` | 
| `Mglob` | `set_domain()` | 
| `TOTAL_TIME` | `set_domain()` | 
| `AMP_WK`| `set_domain()` |
| `DEP_WK` | `set_domain()` |

## Preprocessing of Design Matrix

### Calculation of Dependency Parameters
One standard pipeline is used to calculate the dynamic variables:
```python
function_sets = {'Standard' : [mod.get_hydro,
                               mod.set_domain,
                               mod.set_stations]}
```
####  1: Calculate hydodynamic variables (`get_hydro()`)
[[CODE](./model_code/get_hydro.py)] This function uses the depth and period defined by `DEPTH_FLAT` and `Tperiod` respectively to calculate $k$, $\lambda_0$ and $kh$ using the linear dispersion relation

- **RETURNS**: `k`, `kh`, `L` 


####  2: Set domain regions and wavemaker (`set_domain()`)
[[CODE](./model_code/set_domain.py)] This function applies all of the $\pi$, $\tau$ and $\xi$ to appropriately set the geometry of the tank. `DX` is calculated as described in the List PArameters section

- **RETURNS**: `Sponge_west_width`, `Sponge_east_width`, `Xc_WK`, `DEP_WK`, `AMP_WK`, `Mglob`,`TOTAL_TIME`, `DX`, `DY`

####  3: Set up stations (`set_stations()`)
[[CODE](./model_code/set_stations.py)] This function sets up stations equally spaced at ~1 wavelength apart in the East Region.

- **RETURNS**: None, just ensures station files are printed

### Filter Functions
The is a single filter function:

```python
filter_functions = [fs.filter_kh]
```
which just discards any combination of parameters where $kh>\pi$

### Plot Functions
Nothing is plotted at the generation time.
### Print Functions
Since we are using stations, we need to print out the station files:
```python
print_functions = [fs.print_stations]
```

### Generation Script
Using the [design matrix](./design_matrices/DX_Sens.csv), the generation script is given as [gen.py](./model_pipelines/gen.py)


## Miscellaneous Notes