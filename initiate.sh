#!/bin/bash
# Define run_name
RUN_NAME="test_matrix"

# Define the source and destination directories
SOURCE_DIR="/work/thsu/rschanta/RTS-PY/batch-scripts"
DEST_DIR="/work/thsu/rschanta/RTS-PY/runs/$RUN_NAME"

## Create directories
# File under runs/
mkdir -p "$DEST_DIR"
# File for slurm logs
mkdir -p "$DEST_DIR/logs"
# File for batch scripts
mkdir -p "$DEST_DIR/batch_scripts"
# File for run-specific code (ie- preprocessing)
mkdir -p "$DEST_DIR/model_code"
# File for the main pipeline
mkdir -p "$DEST_DIR/model_pipeline"
# Copy all files from the source directory to the destination directory
cp -r "$SOURCE_DIR"/* "$DEST_DIR/batch_scripts"