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
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/FRF/F5/logs/generate_files/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/FRF/F5/logs/generate_files/err.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/fw_models/FRF/F5/envs/F5.env
    
    ## Activate Python Environment
    conda activate $CONDA_ENV
    
    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/fw_models/FRF/F5/envs/F5.env)
    
    ## Run File
    python "/work/thsu/rschanta/RTS-PY/fw_models/FRF/F5/model_pipelines/gen.py"
    