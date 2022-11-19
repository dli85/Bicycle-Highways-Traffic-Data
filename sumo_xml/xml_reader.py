from bs4 import BeautifulSoup
import pickle
import os

xml_path = 'osm.net.xml'
pickle_file_name = 'street_info.pickle'
info = {}


class StreetData:
    def __init__(self, street_name):
        self.street_name = street_name
        self.id_to_from = {}

    def add_to_id_to_from(self, id, edge_to, edge_from):
        self.id_to_from[id] = (edge_to, edge_from)


def populate_info():
    file = open(xml_path, 'r')
    xml = BeautifulSoup(file, 'lxml')

    edges = xml.find_all('edge')

    for x in edges:
        name = x.get("name")
        if name:
            edge_id = x.get('id')
            to = x.get('to')
            _from = x.get('from')

            if name not in info.keys():
                S = StreetData(name)
                S.add_to_id_to_from(edge_id, to, _from)
                info[name] = S
            else:
                S = info.get(name)
                S.add_to_id_to_from(edge_id, to, _from)


def write_pickle_if_not_exists(file_name):
    if not os.path.exists(file_name):
        f = open(file_name, 'wb')
        pickle.dump(info, f)
        f.close()


def read_pickle(file_name):
    f = open(file_name, 'rb')
    data = pickle.load(f)
    f.close()
    return data


if __name__ == '__main__':
    if not os.path.exists(pickle_file_name):
        populate_info()

    write_pickle_if_not_exists(pickle_file_name)

    data = read_pickle(pickle_file_name)

    for key in data.keys():
        print(key)
        print(data.get(key).id_to_from)

    print(len(data.keys()))
