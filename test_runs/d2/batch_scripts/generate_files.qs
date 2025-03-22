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
#SBATCH --job-name=generate_files
#SBATCH --output=/lustre/scratch/rschanta/test_runs/d2/logs/generate_files/out.out
#SBATCH --error=/lustre/scratch/rschanta/test_runs/d2/logs/generate_files/err.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/test_runs/d2/envs/Try1.env
    
    ## Activate Python Environment
    conda activate $CONDA_ENV
    
    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/test_runs/d2/envs/Try1.env)
    
    ## Run File
    python "/work/thsu/rschanta/RTS-PY/test_runs/d2/pipe/generate.py"
    