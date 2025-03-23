import math
def filter_kh(var_dict):
    
    if var_dict['kh'] > math.pi:
        return False
    else:
        return True
