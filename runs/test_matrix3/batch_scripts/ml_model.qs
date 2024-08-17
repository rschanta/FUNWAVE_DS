#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --job-name=ml_model
#SBATCH --dependency=28262821
#SBATCH --output=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/ml_model/out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/ml_model/err.out
#

    conda activate tf_env
    python /work/thsu/rschanta/RTS-PY/runs/test_matrix3/model_pipelines/p04_ml_model.py /lustre/scratch/rschanta test_matrix3 "test_model"
    