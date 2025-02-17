#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --partition=thsu
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --job-name=generate_files
#SBATCH --output=/lustre/scratch/rschanta/Flat_Tank/Time_Sens/logs/generate_files/out.out
#SBATCH --error=/lustre/scratch/rschanta/Flat_Tank/Time_Sens/logs/generate_files/err.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/envs/Time_Sens.env
    
    ## Activate Python Environment
    conda activate $CONDA_ENV
    
    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/envs/Time_Sens.env)
    
    ## Run File
    python "/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/model_pipelines/gen.py"
    