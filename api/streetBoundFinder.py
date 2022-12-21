import os
from dotenv import load_dotenv
import googlemaps
from pickle_utils import write_pickle_if_not_exists, read_pickle
from StreetData import StreetData
from selenium import webdriver
import time

street_info_pickle_path = "./../sumo_xml/street_info.pkl"

load_dotenv("api.env")
API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE_MAPS')
gmaps = googlemaps.Client(key=API_KEY_GOOGLE)
overall_results = []
streets_possible_coordinates = []

cities = ['Boston', 'Newton', 'Wellesley', 'Weston', 'Brookline',
          'Roxbury', ]

# every item is a tuple: (street name, (origin address, destination address, [waypoint 1, waypoint 2, ...]))
# (string, (string, string, [strings...]))
start_end_waypoints = []

overall_results_file_path = 'street_main_cords_overall_results.pkl'
streets_all_cords_file_path = 'street_main_cords_possible_cords.pkl'

street_types = {'Street', 'St', 'Road', 'Rd'}

# Right edge 42.352941570051286, -71.05632401053465
# Top edge: 42.358287400703084, -71.10959837968905
# Bottom Edge: 42.2850683687529, -71.09142851516339
# Left Edge: 42.30537562165206, -71.31280840343489

#
# Box: top = 42.358287400703084, bottom = 42.2850683687529, left = -71.31280840343489, right = -71.05632401053465
lat_top = 42.358287400703084
lat_bottom = 42.2850683687529
lng_left = -71.31280840343489
lng_right = -71.05632401053465


def street_bound_finder(possible_cords_dict):
    for tuple_elem in possible_cords_dict:
        street_name = tuple_elem[0]
        lat_lng_dicts = tuple_elem[1]
        if len(lat_lng_dicts) == 0:
            start_end_waypoints.append((street_name, None))
        else:
            origin = None
            destination = None
            waypoints = None
            for lat_lng in lat_lng_dicts:
                latitude = lat_lng['lat']
                longitude = lat_lng['lng']
                print(street_name + " " + str(latitude) + ", " + str(longitude))
                if lat_bottom < latitude < lat_top and lng_left < longitude < lng_right:
                    print(str(latitude) + ", " + str(longitude) + "    IN")
                    origin, destination = street_origin_destination_address_finder(latitude, longitude)
                    break
            if origin is None:
                start_end_waypoints.append((street_name, None))
            else:
                waypoints = calculate_waypoints(origin, destination)
                start_end_waypoints.append((street_name, (origin, destination, waypoints)))


# Takes in a latitude and longitude of a street, finds the bounds as addresses
def street_origin_destination_address_finder(lat, lng):
    driver = webdriver.Chrome('./../driver/chromedriver.exe')
    driver.get("https://www.google.com/maps")
    input()
    driver.close()
    return 0, 0


def calculate_waypoints(origin_address, destination_address):
    waypoints = []

    return waypoints


# Uses api call to get initial coordinates for a list of street names
# Google Geocoding Api
def get_initial_cords(list_of_street_names):
    # southwest corner then northeast corner
    bounds = {'southwest': (42.2850683687529, -71.31280840343489),
              "northeast": (42.358287400703084, -71.05632401053465)}
    for street_name in list_of_street_names:
        geocode_result = gmaps.geocode(street_name, bounds=bounds)
        overall_results.append((street_name, geocode_result))

        possible_streets = []
        for result in geocode_result:
            possible_streets.append(result['geometry']['location'])

        streets_possible_coordinates.append((street_name, possible_streets))
        print((street_name, geocode_result))
        print((street_name, possible_streets))
    write_pickle_if_not_exists(overall_results_file_path, overall_results)
    write_pickle_if_not_exists(streets_all_cords_file_path, streets_possible_coordinates)


if __name__ == '__main__':
    data = read_pickle(street_info_pickle_path)
    street_names = data.keys()

    get_initial_cords(street_names)

    # streets_possible_cords = read_pickle('street_main_cords_possible_cords.pkl')
    # street_bound_finder(streets_possible_cords)
