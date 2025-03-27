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
#SBATCH --job-name=postprocess_individual
#SBATCH --output=/lustre/scratch/rschanta/USACE/Flat_Tank/Base_Study/logs/postprocess_individual/out.out
#SBATCH --error=/lustre/scratch/rschanta/USACE/Flat_Tank/Base_Study/logs/postprocess_individual/err.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Base_Study/envs/BASE1.env

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Base_Study/envs/BASE1.env)
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Base_Study/pipe/postprocess_compress.py"

    