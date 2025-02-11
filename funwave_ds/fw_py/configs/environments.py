import os

'''
Tools for obtaining environment variables in python
'''

def get_env_dirs():
    '''
    Get all the environment variables as a dictionary, which
    include the following:
        > WORK_DIR: Work path
        > DATA_DIR: Path for long-term storage
        > TEMP_DIR: Path for temporary storage
        > FW_MODEL: Name of FUNWAVE model
        > RUN_NAME: Run name within model
    '''
    env_vars = {
        "WORK_DIR": os.getenv("WORK_DIR"),
        "DATA_DIR": os.getenv("DATA_DIR"),
        "TEMP_DIR": os.getenv("TEMP_DIR"),
        "LOG_DIR":  os.getenv("LOG_DIR"),
        "FW_MODEL": os.getenv("FW_MODEL"),
        "RUN_NAME": os.getenv("RUN_NAME")
    }
    
    return env_vars
