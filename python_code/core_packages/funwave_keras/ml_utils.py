

def split_paths(train_ratio,files):
    random.shuffle(files)
    split_index = int(len(files) * train_ratio)
    train_set = files[:split_index]
    val_set = files[split_index:]

    return train_set, val_set