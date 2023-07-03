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
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
start_end_waypoints_file_path = 'start_end_waypoints.pkl'

# Amount of seconds to wait
driver_wait = 10

reset_offset = 0

# Box: top = 42.358287400703084, bottom = 42.2850683687529, left = -71.31280840343489, right = -71.05632401053465
lat_top = 42.358287400703084
lat_bottom = 42.2850683687529
lng_left = -71.31280840343489
lng_right = -71.05632401053465


def street_bound_finder(streets_possible_cords_list):
    driver = webdriver.Chrome('./../driver/chromedriver.exe')
    count = 1
    for tuple_elem in streets_possible_cords_list:
        street_name = tuple_elem[0]
        lat_lng_dicts = tuple_elem[1]
        if len(lat_lng_dicts) == 0:
            start_end_waypoints.append((street_name, None))
            print(f'{street_name} completed. {str(count + reset_offset)}/{len(streets_possible_cords_list) + reset_offset}')
        else:
            origin = None
            destination = None
            waypoints = None
            for lat_lng in lat_lng_dicts:
                while True:
                    latitude = lat_lng['lat']
                    longitude = lat_lng['lng']
                    # print(street_name + " " + str(latitude) + ", " + str(longitude))

                    # lower, upper
                    try:
                        driver, origin, destination = street_origin_destination_address_finder(driver, street_name,
                                                                                           latitude, longitude)
                        break
                    except NoSuchElementException:
                        origin = None
                        break
                    except TimeoutException:
                        input("Solve the recapatcha then press enter")
                break
            if origin is None:
                start_end_waypoints.append((street_name, None))
                print(f'{street_name} completed. {count + reset_offset}/{len(streets_possible_cords_list) + reset_offset}')
            else:
                waypoints = calculate_waypoints(origin, destination)
                start_end_waypoints.append((street_name, (origin, destination, waypoints)))
                print(f'{street_name} completed. {count + reset_offset}/{len(streets_possible_cords_list) + reset_offset}')
                print((origin, destination, waypoints))

        if count % 2 == 0:
            write_pickle_if_not_exists(start_end_waypoints_file_path, start_end_waypoints, overwrite=True)
            print(f'Saved up to row {str(count - 1 + reset_offset)}')
        print(f'Completed row {str(count - 1 + reset_offset)}')
        print()
        count += 1

    write_pickle_if_not_exists(start_end_waypoints_file_path, start_end_waypoints, overwrite=True)
    print("Done!")

# Takes in a latitude and longitude of a street, finds the bounds as addresses
def street_origin_destination_address_finder(driver, street_name, lat, lng):
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
    time.sleep(0.5)
    h1_initial_street_name = driver.find_element_by_xpath(
        '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div['
        '1]/div/div/div[2]/div[1]/div[1]/div[1]/h1').text
    time.sleep(0.5)
    # TODO: find the bounds of the street by testing addresses and comparing to h1_initial_street_name

    # Find min address

    # /html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[12]/div/div[1]/span[3]/span[3]
    # containing Add a missing place = address not found
    # containing Suggest an edit = address found

    back_half_address = f'{street_name}, {city}, {state_and_zip}'.format(street_name=street_name,
                                                                         city=city,
                                                                         state_and_zip=state_and_zip)

    # Finding lower bound
    lower_bound_address = None
    address_number = 1
    notFound = True
    while notFound:
        address_to_search = f'{address_number} {back_half_address}'

        if address_number > 1000:
            raise NoSuchElementException

        if address_exists(driver, h1_initial_street_name, address_to_search, searchbar):
            notFound = False
            lower_bound_address = address_to_search
        else:
            address_number += 100

    # Finding upper bound
    lower = address_number
    upper = 10000
    hist = []
    while upper - lower > 100:
        mid = int((lower + upper) / 2)
        address_to_search = f'{mid} {back_half_address}'
        exists = address_exists(driver, h1_initial_street_name, address_to_search, searchbar)
        if exists:
            lower = mid + 1
        else:
            upper = mid - 1
        hist.append((mid, exists))

    for i in range(len(hist) - 1, 0, -1):
        if hist[i][1]:
            mid = hist[i][0]
            break
    upper_bound_address = f'{mid} {back_half_address}'
    # print(lower_bound_address)
    # print(upper_bound_address)
    # print(hist)
    return driver, lower_bound_address, upper_bound_address


def address_exists(driver, street_name, address_to_enter, searchbar):
    searchbar.clear()
    searchbar.send_keys(address_to_enter, Keys.RETURN)
    # Change this to webdriver wait?
    time.sleep(1.5)
    updated_address = driver.find_element_by_xpath('/html/body/div[3]/div[9]/div['
                                                   '9]/div/div/div[1]/div[2] '
                                                   '/div/div[1]/div/div/div[2]/div['
                                                   '1]/div[1]/div[1]/h1').text
    if updated_address == street_name:
        return False
    else:
        return True


# Address should be in the form "<number> <street name>, city, state zipcode"
def calculate_waypoints(origin_address, destination_address):
    origin_address_number = origin_address.split(" ")[0]
    origin_address_back_half = origin_address.replace(origin_address_number + " ", "")
    destination_address_number = destination_address.split(" ")[0]
    destination_address_back_half = destination_address.replace(destination_address_number + " ", "")

    num_waypoints = int(max(int(destination_address_number) / 1000, 1)) * 2
    # print(num_waypoints)

    waypoints = []

    for i in range(num_waypoints):
        new_address_number = int((i + 1) / (num_waypoints + 1) * float(destination_address_number))
        waypoints.append(f'{new_address_number} {origin_address_back_half}')

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
    start_end_waypoints = read_pickle(start_end_waypoints_file_path)
    temp = []
    [temp.append(x) for x in start_end_waypoints if x not in temp]
    start_end_waypoints = temp
    for tup in start_end_waypoints:
        print(tup)

    print(f'You should start at {len(start_end_waypoints)}')
    data = read_pickle(street_info_pickle_path)
    street_names = data.keys()

    streets_possible_cords = read_pickle('street_main_cords_possible_cords.pkl')

    # for tup in streets_possible_cords:
    #     print(tup)

    change_starting_point = input("Change starting point? [y/n] ")
    if change_starting_point.lower().strip() == 'y':
        new_starting_point = int(input(f"Enter the new starting point (0 to {len(streets_possible_cords) - 1}): "))
        streets_possible_cords = streets_possible_cords[new_starting_point:]
        start_end_waypoints = read_pickle(start_end_waypoints_file_path)
        reset_offset = new_starting_point
    street_bound_finder(streets_possible_cords)
