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
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/logs/T1/generate_files/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/logs/T1/generate_files/err.out
#

    ## Activate conda environment
    conda activate tf_env

    ## Export environment variables
    export WORK_DIR=/work/thsu/rschanta/RTS-PY 
    export DATA_DIR=/work/thsu/rschanta/DATA
    export TEMP_DIR=/lustre/scratch/rschanta
    export FW_MODEL=DFR_Pi
    export RUN_NAME=T1

    ## Generate Inputs
    python "/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/model_pipelines/T1/p01_generate_files.py"
    