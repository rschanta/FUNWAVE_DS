#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --job-name=postb
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --output=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/postb/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/postb/err.out
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#

conda activate tf_env
python /work/thsu/rschanta/RTS-PY/runs/test_matrix3/model_pipelines/p03b_postprocess.py /lustre/scratch/rschanta test_matrix3 
