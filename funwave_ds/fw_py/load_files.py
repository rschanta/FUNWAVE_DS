import pickle

def load_input_dict(path,tri_num):
    with open(path, 'rb') as file:
        In_d = pickle.load(file)
    return In_d[f'tri_{tri_num:05}']