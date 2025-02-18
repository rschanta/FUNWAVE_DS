#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --exclude=r03n56
#SBATCH --array=1-216
#SBATCH --job-name=run_condense_outputs
#SBATCH --dependency=29705756
#SBATCH --output=/lustre/scratch/rschanta/USACE/Flat_Tank/Time_Sens/logs/run_condense_outputs/out/out%a.out
#SBATCH --error=/lustre/scratch/rschanta/USACE/Flat_Tank/Time_Sens/logs/run_condense_outputs/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/envs/Time_Sens.env

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$TEMP_DIR/$FW_MODEL/$RUN_NAME/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${input_dir}input_${task_id}.txt"
    
    ## Run FUNWAVE
        ${UD_MPIRUN} $FW_EX "$input_file"

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/envs/Time_Sens.env)
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/model_pipelines/pro.py"

    