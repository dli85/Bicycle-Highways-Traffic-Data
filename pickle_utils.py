import os
import pickle


def write_pickle_if_not_exists(file_name, data, overwrite=False):
    if not overwrite:
        if not os.path.exists(file_name):
            with open(file_name, 'wb') as file:
                pickle.dump(data, file)
    else:
        with open(file_name, 'wb') as file:
            pickle.dump(data, file)


def read_pickle(file_name):
    f = open(file_name, 'rb')
    data = pickle.load(f)
    f.close()
    return data
