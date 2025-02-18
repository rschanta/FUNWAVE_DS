import numpy as np

'''
Filter out by kh: FUNWAVE is only intended for shallow to intermediate
waters, defined by kh < pi
'''

def filter_kh(vars):
    print('\t\tChecking kh...')
    kh = vars['kh']
    T = vars['Tperiod']
    h = vars['DEPTH_FLAT']
   
    if kh > np.pi:
        print(f'\t\tFAIL: Case is in deep water! kh = {kh:.3f}, T = {T:.3f}, h = {h:.3f}')
        return False
    else:
        print(f'\t\tSUCCESS: Case is in shallow/intermediate water!  kh = {kh:.3f}, T = {T:.3f}, h = {h:.3f}')
        return True