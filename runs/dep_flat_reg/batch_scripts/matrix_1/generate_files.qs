#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --job-name=generate_files
#SBATCH --output=/work/thsu/rschanta/RTS-PY/runs/dep_flat_reg/logs/matrix_1/generate_files/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/runs/dep_flat_reg/logs/matrix_1/generate_files/err.out
#

    ## Activate conda environment and compress
    conda activate tf_env
    python "RTS-PY/runs/dep_flat_reg/model_pipelines/matrix_1/p01_generate_files.py" /lustre/scratch/rschanta dep_flat_reg
    