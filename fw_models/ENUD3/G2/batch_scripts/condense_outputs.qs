#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-10
#SBATCH --job-name=condense_outputs
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/ENUD3/G2/logs/condense_outputs/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/ENUD3/G2/logs/condense_outputs/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/fw_models/ENUD3/G2/envs/G2.env

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/fw_models/ENUD3/G2/envs/G2.env)
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "/work/thsu/rschanta/RTS-PY/fw_models/ENUD3/G2/model_pipelines/pro.py"

    