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
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/USACE_Empty_Tank/A2/logs/generate_files/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/USACE_Empty_Tank/A2/logs/generate_files/err.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/fw_models/USACE_Empty_Tank/A2/envs/A2.env
    
    ## Activate Python Environment
    conda activate $CONDA_ENV
    
    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/fw_models/USACE_Empty_Tank/A2/envs/A2.env)
    
    ## Run File
    python "/work/thsu/rschanta/RTS-PY/fw_models/USACE_Empty_Tank/A2/model_pipelines/gen.py"
    