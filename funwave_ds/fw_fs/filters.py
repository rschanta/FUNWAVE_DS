import numpy as np

'''
Filter out by kh: FUNWAVE is only intended for shallow to intermediate
waters, defined by kh < pi
'''

def filter_kh(vars):
    print('\t\tChecking kh...')
    kh = vars['kh']
   
    if kh > np.pi:
        print('\t\tFAIL: Case is in deep water!')
        return False
    else:
        print('\t\tSUCCESS: Case is in shallow/intermediate water!')
        return True