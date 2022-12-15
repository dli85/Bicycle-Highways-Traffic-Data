import os
import pickle


def write_pickle_if_not_exists(file_name, data):
    if not os.path.exists(file_name):
        f = open(file_name, 'wb')
        pickle.dump(data, f)
        f.close()


def read_pickle(file_name):
    f = open(file_name, 'rb')
    data = pickle.load(f)
    f.close()
    return data
