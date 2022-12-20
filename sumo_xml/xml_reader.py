from bs4 import BeautifulSoup
from pickle_utils import write_pickle_if_not_exists, read_pickle
from StreetData import StreetData
import os

xml_path = 'osm.net.xml'
pickle_file_name = 'street_info.pkl'
info = {}


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


if __name__ == '__main__':
    if not os.path.exists(pickle_file_name):
        populate_info()

    write_pickle_if_not_exists(pickle_file_name, info)

    data = read_pickle(pickle_file_name)

    for key in data.keys():
        print(key)
        print(data.get(key).id_to_from)

    print(len(data.keys()))
