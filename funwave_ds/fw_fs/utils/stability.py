

def get_DX_Torres(L,h):
    '''
    Calculate DX for stability as midrange of Torres and Malej 2022
    using wavelength and height
    '''
    DX = (L + 4*h)/120
    return DX