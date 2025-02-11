# `fw_fs`: Function Sets

The `fw_fs` submodule contains *function sets* that may be useful for certain preprocessing and postprocessing pipelines. They are broadly divided by general function:

|File| Purpose|
|:--|:--|
|[animation](./animation) | Create animations of FUNWAVE-TVD outputs from `.nc` formats as specified in `fw_py`| 
|[filters](./filters) | Common filters to exclude invalid inputs (ie- deep water modeling) | 
|[model_utils](./model_utils) | Tools that may be useful for specific modes of FUNWAVE-TVD, such as `DEPTH_TYPE=SLP`| 
|[plots](./plots) | Create static diagrams (pngs, jpegs, etc) for bathymetry, spectra, etc. | 
|[prints](./prints) | Print supporting input files that models may need, such as `bathy.txt` or `WaveCompFile.txt`| 
|[wave_forcing](./wave_forcing) | Functionality for wavemakers, coupling, or any forcing terms| 