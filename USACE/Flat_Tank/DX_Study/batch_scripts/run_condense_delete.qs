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
#SBATCH --array=1-408
#SBATCH --job-name=run_condense_delete
#SBATCH --output=/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/logs/run_condense_delete/out/out%a.out
#SBATCH --error=/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/logs/run_condense_delete/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Study/envs/BASE1.env

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
    export $(xargs </work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Study/envs/BASE1.env)
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    export FUNC_NAME=run_condense_delete
    
    ## Run the Compression File
    python "/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Study/pipe/pro.py"

    ## Run the Raw Output Deletions
    
    echo "Deleting Raw Outputs from: ${or}/out_raw_${task_id}"
    rm -rf "${or}/out_raw_${task_id}"
  
    