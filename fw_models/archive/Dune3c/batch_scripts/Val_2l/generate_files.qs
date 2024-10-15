#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --job-name=generate_files
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/Dune3c/logs/Val_2l/generate_files/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/Dune3c/logs/Val_2l/generate_files/err.out
#

    ## Activate conda environment
    conda activate tf_env

    ## Export environment variables
    export WORK_DIR=/work/thsu/rschanta/RTS-PY 
    export DATA_DIR=/work/thsu/rschanta/DATA
    export TEMP_DIR=/lustre/scratch/rschanta
    export FW_MODEL=Dune3c
    export RUN_NAME=Val_2l

    ## Generate Inputs
    python "/work/thsu/rschanta/RTS-PY/fw_models/Dune3c/model_pipelines/Val_2l/p01_generate_files.py"
    