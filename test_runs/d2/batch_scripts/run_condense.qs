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
#SBATCH --array=1-5
#SBATCH --job-name=run_condense
#SBATCH --dependency=29917494
#SBATCH --output=/lustre/scratch/rschanta/test_runs/d2/logs/run_condense/out/out%a.out
#SBATCH --error=/lustre/scratch/rschanta/test_runs/d2/logs/run_condense/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/test_runs/d2/envs/Try1.env

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$in"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${input_dir}/input_${task_id}.txt"
    
    ## Run FUNWAVE
        ${UD_MPIRUN} $FW_ex "$input_file"

    ## Activate Python Environment
    conda activate $conda

    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/test_runs/d2/envs/Try1.env)
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "/work/thsu/rschanta/RTS-PY/test_runs/d2/pipe/pro.py"

    