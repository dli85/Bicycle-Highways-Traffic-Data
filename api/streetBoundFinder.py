import os
from dotenv import load_dotenv
import googlemaps
from pickle_utils import write_pickle_if_not_exists, read_pickle
from StreetData import StreetData
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

street_info_pickle_path = "./../sumo_xml/street_info.pkl"

load_dotenv("api.env")
API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE_MAPS')
gmaps = googlemaps.Client(key=API_KEY_GOOGLE)
overall_results = []
streets_possible_coordinates = []

# every item is a tuple: (street name, (origin address, destination address, [waypoint 1, waypoint 2, ...]))
# (string, (string, string, [strings...]))
start_end_waypoints = []

overall_results_file_path = 'street_main_cords_overall_results.pkl'
streets_all_cords_file_path = 'street_main_cords_possible_cords.pkl'

street_types = {'Street', 'St', 'Road', 'Rd'}

# Amount of seconds to wait
driver_wait = 10

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

                origin, destination = street_origin_destination_address_finder(street_name, latitude, longitude)
                break
            if origin is None:
                start_end_waypoints.append((street_name, None))
            else:
                waypoints = calculate_waypoints(origin, destination)
                start_end_waypoints.append((street_name, (origin, destination, waypoints)))


# Takes in a latitude and longitude of a street, finds the bounds as addresses
def street_origin_destination_address_finder(street_name, lat, lng):
    driver = webdriver.Chrome('./../driver/chromedriver.exe')
    driver.get("https://www.google.com/maps")

    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchboxinput"]'))) \
        .click()
    searchbar = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    searchbar.send_keys(f'{lat}, {lng}'.format(lat=lat, lng=lng), Keys.RETURN)
    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH,
                                                                         '/html/body/div[3]/div['
                                                                         '9]/div[9]/div/div/div['
                                                                         '1]/div[2]/div/div['
                                                                         '1]/div/div/div[10]/div/div['
                                                                         '1]/span[3]/span[3]')))

    nearby_address = driver.find_element_by_xpath('/html/body/div[3]/div['
                                                  '9]/div[9]/div/div/div['
                                                  '1]/div[2]/div/div['
                                                  '1]/div/div/div[10]/div/div['
                                                  '1]/span[3]/span[3]').text

    h1_street_name_xpath = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[' \
                           '1]/div[1]/div[1]/h1 '

    nearby_address_arr = nearby_address.split(',')
    city = nearby_address_arr[-2:][0].strip()
    state_and_zip = nearby_address_arr[-2:][1].strip()

    h1_initial_cords = driver.find_element_by_xpath(h1_street_name_xpath).text

    street_address_no_numbers = f'{street_name}, {city}, {state_and_zip}'.format(street_name=street_name,
                                                                                 city=city,
                                                                                 state_and_zip=state_and_zip)

    searchbar.clear()
    searchbar.send_keys(street_address_no_numbers, Keys.RETURN)
    # This is the default street name. It comes up when you search for the street with no address or if the address
    # is invalid: (i.e. 10000 Huntington Ave)

    WebDriverWait(driver, driver_wait).until_not(
        EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]'
                                                    '/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1'),
                                         h1_initial_cords))

    h1_initial_street_name = driver.find_element_by_xpath(
        '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div['
        '1]/div/div/div[2]/div[1]/div[1]/div[1]/h1').text

    print(city)
    print(state_and_zip)
    print(h1_initial_street_name)
    # TODO: find the bounds of the street by testing addresses and comparing to h1_initial_street_name

    input()
    driver.close()
    return "1600 pennsylvania ave", "1 Huntington ave"


# Address should be in the form "<number> <street name>, city, state zipcode"
def calculate_waypoints(origin_address, destination_address):
    waypoints = []

    # TODO: get waypoints using binary search. I.e. 1 Huntington avenue to 3700 Huntington avenue should produce
    #  [1000 Huntington avenue, 2000, huntington avenue, 3000 huntington avenue]. Don't need to be complete, just need
    #  to ensure that the polyline goes through the road.

    return waypoints


# Uses api call to get initial coordinates for a list of street names
# Google Geocoding Api
def get_initial_cords(list_of_street_names):
    # southwest corner then northeast corner
    bounds = {'southwest': (lat_bottom, lng_left),
              "northeast": (lat_top, lng_right)}
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

    streets_possible_cords = read_pickle('street_main_cords_possible_cords.pkl')

    # for tup in streets_possible_cords:
    #     print(tup)

    street_bound_finder(streets_possible_cords)
