import random
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from pickle_utils import read_pickle
from StreetData import StreetData

# maximum trips per street
number_of_trips = 40000

new_file_name = 'osm.passenger.trips.demo.xml'
v_type = 'veh_passenger'
street_info_pickle_file_path = '../sumo_xml/street_info.pkl'
depart_increment = 0.9


def write_xml(filename, root):
    xml_string = ET.tostring(root, encoding="unicode")
    soup = BeautifulSoup(xml_string, "xml")
    pretty = soup.prettify()

    with open(filename, 'w') as f:
        f.write(pretty)


if __name__ == '__main__':
    tree = ET.parse("osm.passenger.trips.blank.xml")
    root = tree.getroot()

    street_info = read_pickle(street_info_pickle_file_path)

    init_depart = 0

    street_name_edge_ids = {}

    for key in street_info.keys():
        sd = street_info.get(key)
        street_name_edge_ids[key] = sd.car_edges
        print(key, sd.car_edges)
    input()

    # sorts dictionary by number of edges
    # turns it into a list of tuples
    street_name_edge_ids = sorted(street_name_edge_ids.items(), key=lambda x: len(x[1]), reverse=True)

    trip_counts = []
    for i, (street, edges) in enumerate(street_name_edge_ids):
        trip_count = int(number_of_trips * (len(edges) / sum(len(edges) if len(edges) >= 5 else 0 for _, edges in street_name_edge_ids)))
        # trip_count = int(number_of_trips * (len(street_name_edge_ids) - i) / len(street_name_edge_ids))
        print(street, trip_count)
        trip_counts.append((street, trip_count, edges))

    sum = 0
    for street, trip_count, edges in trip_counts:
        sum += trip_count
    print(sum)
    input()

    trip_id = 'veh'
    trip_id_count = 0
    for street, trip_count, edges in trip_counts:
        for i in range(trip_count):
            init_depart += depart_increment
            trip = ET.SubElement(root, "trip")
            trip.set("id", f"{trip_id}{trip_id_count}")
            trip.set("depart", str(round(init_depart, 2)))
            trip.set("type", v_type)
            trip.set("departLane", "best")
            trip.set("from", random.choice(edges))

            destination = random.choice(edges) if edges else random.choice(random.choice(street_name_edge_ids)[1])
            trip.set("to", destination)
            trip_id_count += 1
    write_xml(new_file_name, root)
