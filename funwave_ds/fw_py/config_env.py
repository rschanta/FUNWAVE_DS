import os

'''
Tools for obtaining environment variables in python
'''

def get_env_dirs():
    env_vars = {
        "WORK_DIR": os.getenv("WORK_DIR"),
        "DATA_DIR": os.getenv("DATA_DIR"),
        "TEMP_DIR": os.getenv("TEMP_DIR"),
        "FW_MODEL": os.getenv("FW_MODEL"),
        "RUN_NAME": os.getenv("RUN_NAME")
    }
    
    return env_vars
