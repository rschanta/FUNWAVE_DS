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
#SBATCH --array=1-25
#SBATCH --job-name=condense
#SBATCH --dependency=29890929
#SBATCH --output=/work/thsu/rschanta/RTS-PY/CIEG_682/Round1/Periodic/logs/condense/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/CIEG_682/Round1/Periodic/logs/condense/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/CIEG_682/Round1/Periodic/envs/Periodic.env

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/CIEG_682/Round1/Periodic/envs/Periodic.env)
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "/work/thsu/rschanta/RTS-PY/CIEG_682/Round1/Periodic/model_pipelines/pro.py"

    