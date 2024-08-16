#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --job-name=gen
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --output=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/gen/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/gen/err.out
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#

## Activate conda environment and compress
conda activate tf_env
python /work/thsu/rschanta/RTS-PY/runs/test_matrix3/model_pipelines/p01_gen_files.py /lustre/scratch/rschanta test_matrix3 
