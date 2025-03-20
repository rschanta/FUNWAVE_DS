import funwave_ds as fwd
import os


base = r'/work/thsu/rschanta/RTS-PY'
dbase = r'/lustre/scratch/rschanta'
lustre = r'/lustre/scratch/rschanta'

d = {
     'WORK_DIR': os.path.join(base,'USACE'),
     'DATA_DIR': os.path.join(dbase,'USACE'),
     'TEMP_DIR': os.path.join(lustre,'USACE'),
     'FW_MODEL': 'Flat_Tank',
     'RUN_NAME': 'Cd_Study',
     'FW_EX': "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
     'CONDA_ENV': "tf_env"}


fwd.setup_model_run(**d)