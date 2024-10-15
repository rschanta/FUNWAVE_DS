#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=thsu
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-576
#SBATCH --job-name=run_ML_preproc2
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/logs/TMA2/run_ML_preproc2/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/logs/TMA2/run_ML_preproc2/err/err%a.out
#

    ## Activate conda environment
    conda activate tf_env

    ## Export environment variables
    export WORK_DIR=/work/thsu/rschanta/RTS-PY 
    export DATA_DIR=/work/thsu/rschanta/DATA
    export TEMP_DIR=/lustre/scratch/rschanta
    export FW_MODEL=DFR_Pi
    export RUN_NAME=TMA2
    export TRI_NUM=$SLURM_ARRAY_TASK_ID

    ## Generate Inputs
    python "/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/model_pipelines/TMA2/p03a_postprocess.py"
    