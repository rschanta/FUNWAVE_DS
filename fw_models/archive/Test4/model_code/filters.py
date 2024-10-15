import numpy as np
def filter_kh(vars):
    print('\t\tChecking kh...')
    kh = vars['kh']
   
    if kh > np.pi:
        print('\t\tFAIL: Case is in deep water!')
        return False
    else:
        print('\t\tSUCCESS: Case is in shallow/intermediate water!')
        return True

    
