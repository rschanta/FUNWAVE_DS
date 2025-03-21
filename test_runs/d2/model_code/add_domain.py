import numpy as np
#%% FUNCTIONS TO ADD DATA TO EACH SIDE OF THE DOMAIN
def append_data_west(A,x):
    first_col = A[:, [0]]  
    A_expanded_cols = np.hstack((np.tile(first_col, (1, x)), A))
    return A_expanded_cols

def append_data_south(A,x):
    first_row = A[[0], :]  # Extract first row (keeping 2D shape)
    A_expanded = np.vstack((np.tile(first_row, (x, 1)), A))
    return A_expanded

def append_data_north(A,x):
    last_row = A[[-1], :]  # Extract last row (keeping 2D shape)
    A_expanded = np.vstack((A, np.tile(last_row, (x, 1))))
    return A_expanded