import math
def filter_kh(var_dict):
    # Unpack Variables-------------------------------------------------
    kh = var_dict['kh']
    #-----------------------------------------------------------------
    print('\t\tChecking if in Deep Water...')

    if kh > math.pi:
        print('\t\tWithin Deep Water!')
        return False
    else:
        print('\t\tWithin Shallow/Intermediate Water!')
        return True


def filter_L70(var_dict):
    # Unpack Variables-------------------------------------------------
    L = var_dict['L']
    h = var_dict['DEPTH_FLAT']
    #-----------------------------------------------------------------
    print('\t\tChecking if in Deep Water...')

    if L/70 < h/15:
        print('\t\tL/70 (DX here) is greater than h/15!')
        return False
    else:
        print('\t\tL/70 (DX here) is less than h/15. Should be fine.')
        return True
