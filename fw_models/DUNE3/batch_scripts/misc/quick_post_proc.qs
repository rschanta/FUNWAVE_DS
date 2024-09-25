#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-1260
#SBATCH --job-name=POSTPROCESS
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/logs/SW1/misc/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/logs/SW1/misc/err/err%a.out
#

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/model_code/postproc_swa.py"

    