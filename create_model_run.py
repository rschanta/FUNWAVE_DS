import funwave_ds as fwd
import os

base = r'/work/thsu/rschanta/RTS-PY/'
wbase = r'/work/thsu/rschanta/'
lbase = r'/lustre/scratch/rschanta/'

d = {
     'WORK_DIR': os.path.join(base,'USACE'),
     'DATA_DIR': os.path.join(wbase,'USACE_Outputs'),
     'TEMP_DIR': os.path.join(lbase,'USACE'),
     'FW_MODEL': 'Flat_Tank',
     'RUN_NAME': 'DX_Sens',
     'FW_EX': "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
     'CONDA_ENV': "tf_env"}


fwd.setup_model_run(**d)