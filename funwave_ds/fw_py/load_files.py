import pickle
import funwave_ds.fw_py as fpy
import os

def load_input_dict():
    p = fpy.get_FW_paths()
    tri_num = os.getenv('TRI_NUM')

    file = open(p['Id'], 'rb')
    try:
        In_d = pickle.load(file)
    finally:
        file.close()  # Ensure the file is closed
    return In_d[f'tri_{int(tri_num):05}']


def load_input_dict_i():
    ptr = fpy.get_FW_tri_paths(tri_num=None)


    with open(ptr['i_file_pkl'], 'rb') as file:
        data = pickle.load(file)
    
    return data