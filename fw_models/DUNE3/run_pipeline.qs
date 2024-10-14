#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --job-name=send_in
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/logs/T01/generate_files/out1.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/logs/T01/generate_files/err1.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/fw_models/DUNE3/envs/T01.env
    
    ## Activate Python Environment
    conda activate $CONDA_ENV
    
    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/fw_models/DUNE3/envs/T01.env)
    
    ## Run File
    python "/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/run_pipeline.py"
    