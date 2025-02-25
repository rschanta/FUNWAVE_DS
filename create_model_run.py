import funwave_ds as fwd
import os


base = r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS'
dbase = r'C:\Users\rschanta\HPC_Pretend'
lustre = r'C:\Users\rschanta\HPC_Pretend'

d = {
     'WORK_DIR': os.path.join(base,'USACE'),
     'DATA_DIR': os.path.join(dbase,'USACE'),
     'TEMP_DIR': os.path.join(lustre,'USACE'),
     'FW_MODEL': 'TRAP_BW',
     'RUN_NAME': '_',
     'FW_EX': "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
     'CONDA_ENV': "tf_env"}


fwd.setup_model_run(**d)