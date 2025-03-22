import numpy as np
def filter_kh(var_dict):
    print(var_dict['kh'])
    if var_dict['kh'] > np.pi:
        return False
    else:
        return True