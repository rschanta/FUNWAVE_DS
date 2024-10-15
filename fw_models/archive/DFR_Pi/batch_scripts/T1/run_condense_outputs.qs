#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-1296
#SBATCH --job-name=run_condense_outputs
#SBATCH --dependency=28302006
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/logs/T1/run_condense_outputs/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/logs/T1/run_condense_outputs/err/err%a.out
#

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    ## Construct name of file
        input_dir="/lustre/scratch/rschanta/DFR_Pi/T1/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${input_dir}input_${task_id}.txt"
    ## Run FUNWAVE
        ${UD_MPIRUN} /work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG "$input_file"

    ## COMPRESS
    conda activate tf_env
    export WORK_DIR=/work/thsu/rschanta/RTS-PY 
    export DATA_DIR=/work/thsu/rschanta/DATA
    export TEMP_DIR=/lustre/scratch/rschanta
    export FW_MODEL=DFR_Pi
    export RUN_NAME=T1
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "/work/thsu/rschanta/RTS-PY/fw_models/DFR_Pi/model_pipelines/T1/p02_run_condense.py"

    ## Remove Raw Folder

    