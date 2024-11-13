# `fw_py`: Core Python Functionality

The `fw_py` submodule contains core functionality of the FUNWAVE_DS package, including the processing of design matrices and their conversion into valid FUNWAVE inputs. This includes the execution of preprocessing steps from design matrices, generation of input files (ie- *input.txt*, spectra files, bathymetry files, etc.), directory creation, logging of metadata, and other miscellaneous helper functions.

## The Configuration Scripts
The scripts beginning with `config_` contain functionality to set up python paths, environmental variables, and logs. This is the necessary "behind the scenes" work to ensure that all files, paths, and packages exist in the correct location and form. These contain many useful helper functions to get the path associated with a specific file (ie- the `input.txt` file for a given FUNWAVE run) without having to remember the entire path.

|File| Purpose|Functions within|
|:--|:--|:--|
|[config_env](./config_env.py) |  | | 
|[config_paths](./config_paths.py) | Tools to get paths | | 
|[config_record](./config_record.py) | | 

## The Design Matrix Scripts
The scripts beginning with `dmatrix_` contain functionality to set process the design matrices and ultimately output the FUNWAVE `input.txt` files en masse. Most of the functions within do not need to be useful directly, rather just the `dmatrix_main.py` file calls the rest.

## The NETCDF Scripts
The scripts beginning with `nc_` contain functionality to needed to "massage" the inputs and outputs of the FUNWAVE models into netcdf forms. Note that there can be some level of complexity in managing netcdf's in Python in different packages, so package control is crucial.

## The Utility Scripts
Broadly, any other functionality is relegated to `utils_` scripts.