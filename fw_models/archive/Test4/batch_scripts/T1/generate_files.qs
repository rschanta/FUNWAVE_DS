#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --job-name=generate_files
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/Test4/logs/T1/generate_files/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/Test4/logs/T1/generate_files/err.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/fw_models/Test4/envs/Test4_debug.env
    
    ## Activate Python Environment
    conda activate $CONDA_ENV
    
    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/fw_models/Test4/envs/Test4_debug.env)
    
    ## Run File
    python "/work/thsu/rschanta/RTS-PY/fw_models/Test4/model_pipelines/T1/p01_generate_files.py"
    