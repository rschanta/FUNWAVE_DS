# `fw_fs`: Function Sets

The `fw_fs` submodule contains *function sets* related to specific preprocessing or postprocessing steps in a pipeline. Although most pipelines are specific to a given model run, there are some particularly common operations that are defined here. 

|File| Purpose|Functions within|
|:--|:--|:--|
|[animate_backgrounds](./animate_backgrounds.py) | Common templates for creating animations of output data, such as $\eta$ vs. $t$ in the domain. | `animate_1D_Var`, `animate_2D_Var`| 
|[animate](./animate.py) | Functions to animate specific output parameters from the templates in animate_backgrounds| `animate_1D_eta`, `animate_1D_u`, `animate_1D_v` | 
|[filters](./filters.py) | Common filters to exclude invalid inputs (ie- deep water modeling) | `filter_kh` | 
|[plots](./plots.py) | Functions to generate commonly-used plots (ie- bathymetry, spectra)| `plot_1D_bathy`, `plot_TS_spectra`| 