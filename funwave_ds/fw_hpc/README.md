# `fw_hpc`: High Performance Computing (HPC) Functionality

The `fw_hpc` submodule contains functionality to run the FUNWAVE_DS module in an HPC system using the SLURM workload manager. Note that this workflow was developed on the Caviness HPC System at the University of Delaware, and the design of this process was guided by the constraints of this system. Notably, specifics concerning the FORTRAN compiler and MPI setup may differ considerably between systems. It is assumed that python scripts can be run via a conda virtual environment to initiate jobs and perform necessary pre/post processing. 


|File| Purpose|Functions/classes within|
|:--|:--|:--|
|[slurm_bodies](./slurm_bodies.py) | Bodies to slurm scripts for various parts of the FUNWAVE_DS workflow.| `load_FW_design_matrix`, `group_variables`,`add_extra_values`, `add_dependent_values`, `apply_filters`, `print_supporting_file`, `plot_supporting_file`, `write_files2`| 
|[slurm_pipeline](./load_files.py) | The pipeline class used to automatically generate `.qs` batch scripts to run jobs in the SLURM workload manager | `SlurmPipeline` | 
|[slurm_utils](./path_tools.py) | List and create all paths used within a FUNWAVE run. Useful for consistency in path names | `get_FW_paths`, `make_FW_paths`,`get_FW_tri_paths` | 
