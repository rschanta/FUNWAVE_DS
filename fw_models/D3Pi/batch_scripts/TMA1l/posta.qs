#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-760
#SBATCH --job-name=posta
#SBATCH --dependency=28317230
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/D3Pi/logs/TMA1l/posta/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/D3Pi/logs/TMA1l/posta/err/err%a.out
#

    ## COMPRESS
    conda activate tf_env
    export WORK_DIR=/work/thsu/rschanta/RTS-PY 
    export DATA_DIR=/work/thsu/rschanta/DATA
    export TEMP_DIR=/lustre/scratch/rschanta
    export FW_MODEL=D3Pi
    export RUN_NAME=TMA1l
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "/work/thsu/rschanta/RTS-PY/fw_models/D3Pi/model_pipelines/TMA1l/p03a_postprocess.py"

    ## Remove Raw Folder

    