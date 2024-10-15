# `fw_py`: Core Python Functionality

The `fw_py` submodule contains core functionality of the FUNWAVE_DS package, including the processing of design matrices and their conversion into valid FUNWAVE inputs. This includes the execution of preprocessing steps from design matrices, generation of input files (ie- *input.txt*, spectra files, bathymetry files, etc.), directory creation, logging of metadata, and other miscellaneous helper functions.

|File| Purpose|Functions within|
|:--|:--|:--|
|[design_matrix](./design_matrix.py) | Processing pipeline on a design matrix to generate `input.txt` files | `load_FW_design_matrix`, `group_variables`,`add_extra_values`, `add_dependent_values`, `apply_filters`, `print_supporting_file`, `plot_supporting_file`, `write_files2`| 
|[environments](./environments.py) | Tools to get environment variables | `get_env_dirs`| 
|[load_files](./load_files.py) | Load in input summary files for a given run. Useful for post-processing. | `load_input_dict`, `load_input_dict_i` | 
|[path_tools](./path_tools.py) | List and create all paths used within a FUNWAVE run. Useful for consistency in path names | `get_FW_paths`, `make_FW_paths`,`get_FW_tri_paths` | 
|[print_files](./print_files.py) | print an `input.txt` file, a `DEPTH_FILE`, or a spectra file according to FUNWAVE requirements.| `print_input_file`, `print_time_series_spectra_file`, `print_bathy_file`| 
|[utils](./utils.py) | miscellaneous utility functions| `convert_to_number`| 