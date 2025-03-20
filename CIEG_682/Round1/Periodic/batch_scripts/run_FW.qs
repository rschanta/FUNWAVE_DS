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
#SBATCH --array=3-10
#SBATCH --job-name=run_FW
#SBATCH --dependency=29891106
#SBATCH --output=/work/thsu/rschanta/RTS-PY/CIEG_682/Round1/Periodic/logs/run_FW/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/CIEG_682/Round1/Periodic/logs/run_FW/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/CIEG_682/Round1/Periodic/envs/Periodic.env

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$TEMP_DIR/$FW_MODEL/$RUN_NAME/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${input_dir}input_${task_id}.txt"
    
    ## Run FUNWAVE
        ${UD_MPIRUN} $FW_EX "$input_file"


    