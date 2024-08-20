import pickle
import funwave_ds.fw_ba as fba
import funwave_ds.fw_py as fpy
import os
def load_input_dict(path,tri_num):
    with open(path, 'rb') as file:
        In_d = pickle.load(file)
    return In_d[f'tri_{tri_num:05}']


def load_input_dict2():
    p = fpy.get_FW_paths2()
    tri_num = os.getenv('TRI_NUM')

    file = open(p['Id'], 'rb')
    try:
        In_d = pickle.load(file)
    finally:
        file.close()  # Ensure the file is closed
    return In_d[f'tri_{int(tri_num):05}']