#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --job-name=postb
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/D3Pi/logs/TMA1/postb/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/D3Pi/logs/TMA1/postb/err.out
#

    ## Activate conda environment
    conda activate tf_env

    ## Export environment variables
    export WORK_DIR=/work/thsu/rschanta/RTS-PY 
    export DATA_DIR=/work/thsu/rschanta/DATA
    export TEMP_DIR=/lustre/scratch/rschanta
    export FW_MODEL=D3Pi
    export RUN_NAME=TMA1

    ## Generate Inputs
    python "/work/thsu/rschanta/RTS-PY/fw_models/D3Pi/model_pipelines/TMA1/p03b_postprocess.py"
    