# Environment Variables/Project Organization
The `FUNWAVE_DS` module makes frequent use of environment variables to specify key directories that given processes may need. 


## Project Organization
There are 2 levels of organization built into the module:
- `FW_MODEL`: represents a larger class of FUNWAVE projects.
    	
    - `RUN_NAME`: a subproject within the larger `FW_MODEL` that contains some ensemble of FUNWAVE runs.

For example, suppose we have a project modeling the Delaware Bay, and we want to run a few sensitivity analyses for input parameters like `DX`, `Delta_WK` and `Sponge_west_width`, and then also run a batch of simulations for January conditions and June conditions. The project structure may look something like this:

```
DELAWARE_BAY/
├── DX_SENS
├── Delta_WK_SENS
├── Sponge_SENS
├── Jan_Wave_Conds
└── May_Wave_Conds
```

where *DELAWARE_BAY* is the `FW_MODEL` and the 5 subdirectories are the `RUN_NAME`s specified. Each `RUN_NAME` contains code to run an ensemble of models. For example, the first three may try out different values of `DX`, `Delta_WK` and `Sponge_west_width`, and the last two may specify a different model for each day of the month. This keeps the larger ensembles of runs organized by project type and individual research questions.
## Directories
There are 3 main directories that are leveraged through the FUNWAVE_DS module.

- `WORK_DIR`: (*Working Directory*): This directory is intended to contain all the code, design matrices, logs, environment files, etc. specifying a given ensemble of FUNWAVE runs. 
- `TEMP_DIR`: (*Temporary Storage Directory*): This directory is intended for intermediate FUNWAVE outputs before file compression and post-processing. The raw binary outputs of FUNWAVE models (the contents of `RESULT_FOLDER`) are intended to be placed here before eventual deletion. For running large ensembles, this should be on a system that can handle massive file i/o operations, such as Lustre.
- `DATA_DIR`: (*Long Term Storage Directory*): This directory is intended for FUNWAVE inputs/outputs that are to be kept long-term, included post-processed inputs/outputs. This should be on a system that has a large storage volume.

### Structure of the Working Directory
Suppose `WORK_DIR=/home/FW_PROJECTS`, `FW_MODEL=DELAWARE_BAY` as before, and that we are working on the run for January conditions, `RUN_NAME=Jan_Wave_Conds`. The directory structure created is the following:
```
FW_PROJECTS/
└── DELAWARE_BAY/
    └── Jan_Wave_Conds/
        ├── batch_scripts/
        ├── design_matrices/
        ├── envs/
        ├── logs/
        ├── model_code/
        └── model_pipelines/
      
```

where:
- `batch_scripts`: intended to hold HPC batch scripts associated with this run
- `design_matrices`: intended to hold any design matrices used in the development of the run
- `envs`: intended to hold and `.env` files for this run
- `logs`: used for log files from HPC outputs
- `model_code`: used for code *specific* to this given run configuration. This should be packaged into a Python module with an `__init__.py` file
- `model_pipelines`: used to specify the actual python code to be executed

## FUNWAVE Executable
Of course, every FUNWAVE run relies on the compiled source code that may be different, depending on the version and modules of FUNWAVE used. This is tracked by the `FW_EX` environment variable.

## Conda Environment
The conda environment being used should be included under the `CONDA_ENV` environment variable.