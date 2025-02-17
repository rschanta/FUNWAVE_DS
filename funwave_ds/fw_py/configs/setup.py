import os

def setup_model_run(WORK_DIR=None,
                    DATA_DIR = None,
                    TEMP_DIR = None,
                    FW_MODEL=None,
                    RUN_NAME=None,
                    FW_EX = None,
                    CONDA_ENV=None):

    # Define the subfolders to create
    subfolders = ["design_matrices", 
                  "logs", 
                  "batch_scripts", 
                  "model_code", 
                  "model_pipelines",
                  "envs"]


    # Create directory for WORK_DIR/FW_MODEL/RUN_NAME
    base_dir = os.path.join(WORK_DIR, FW_MODEL,RUN_NAME)
    os.makedirs(base_dir, exist_ok=True)

    # Create each subfolder within WORK_DIR/FW_MODEL/RUN_NAME
    for folder in subfolders:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

    print(f"Created {FW_MODEL} folder with subdirectories: {', '.join(subfolders)}")

    # Path to Environment File
    env_file_path = os.path.join(base_dir, 'envs',f'{RUN_NAME}.env')
    
    ## Contents of Environment File
    dotenv_file = f"""WORK_DIR={WORK_DIR}
    DATA_DIR={DATA_DIR}
    TEMP_DIR={TEMP_DIR}
    FW_MODEL={FW_MODEL}
    RUN_NAME={RUN_NAME}
    LOG_DIR={WORK_DIR}/fw_models/{FW_MODEL}/{RUN_NAME}/logs
    ENV_FILE_PATH={env_file_path}
    PYTHONPATH={WORK_DIR}:{WORK_DIR}/{FW_MODEL}/{RUN_NAME}
    FW_EX={FW_EX}
    CONDA_ENV={CONDA_ENV}
    """
    
    # Write Environment File
    with open(env_file_path, "w") as file:
        file.write(dotenv_file)
        
    print(f"Wrote .env file to {env_file_path}")
    return
