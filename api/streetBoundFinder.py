import os
from dotenv import load_dotenv
import googlemaps
from pickle_utils import write_pickle_if_not_exists, read_pickle
from StreetData import StreetData

street_info_pickle_path = "./../sumo_xml/street_info.pkl"

load_dotenv("api.env")
API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE_MAPS')
gmaps = googlemaps.Client(key=API_KEY_GOOGLE)
overall_results = []
streets_all_cords = []

overall_results_file_path = 'street_main_cords_overall_results.pkl'
streets_all_cords_file_path = 'street_main_cords_possible_cords.pkl'

# Right edge 42.352941570051286, -71.05632401053465
# Top edge: 42.358287400703084, -71.10959837968905
# Bottom Edge: 42.2850683687529, -71.09142851516339
# Left Edge: 42.30537562165206, -71.31280840343489


def street_bound_finder():
    pass


# Uses api call to get initial coordinates for a list of street names
# Google Geocoding Api
def get_initial_cords(list_of_street_names):
    for street_name in list_of_street_names:
        geocode_result = gmaps.geocode(street_name + ", MA")
        overall_results.append((street_name, geocode_result))

        possible_streets = []
        for result in geocode_result:
            possible_streets.append(result['geometry']['location'])

        streets_all_cords.append((street_name, possible_streets))
        print((street_name, geocode_result))
        print((street_name, possible_streets))

    write_pickle_if_not_exists(overall_results_file_path, overall_results)
    write_pickle_if_not_exists(streets_all_cords_file_path, streets_all_cords)


if __name__ == '__main__':
    data = read_pickle(street_info_pickle_path)
    street_names = data.keys()

    streets_all_cords = read_pickle('street_main_cords_possible_cords.pkl')

    for elem in streets_all_cords:
        print(elem)
    print(len(streets_all_cords))
