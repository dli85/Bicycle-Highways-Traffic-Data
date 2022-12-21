import os
from dotenv import load_dotenv
import googlemaps
import requests
import polyline

load_dotenv("api.env")
API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE_MAPS')
API_KEY_MAP_QUEST = os.getenv('API_KEY_MAP_QUEST')

street_name = "Huntington Avenue, Boston, MA"
gmaps = googlemaps.Client(key=API_KEY_GOOGLE)


# Not needed
def get_street_bounds(name_of_street):
    geocode_result = gmaps.geocode(name_of_street)

    endpoint_1 = geocode_result[0]['geometry']['location']
    endpoint_2 = geocode_result[0]['geometry']['viewport']

    print(f"Endpoint 1: {endpoint_1['lat']}, {endpoint_1['lng']}")
    print(f"Endpoint 2: {endpoint_2['northeast']['lat']}, {endpoint_2['northeast']['lng']}")
    print(f"Endpoint 3: {endpoint_2['southwest']['lat']}, {endpoint_2['southwest']['lng']}")

    return endpoint_2['southwest']['lat'], endpoint_2['southwest']['lng'], \
        endpoint_2['northeast']['lat'], endpoint_2['northeast']['lng'],


# Not needed
def map_quest_get_bounds(name_of_street):
    api_key = API_KEY_MAP_QUEST

    # Set the street name, city, and state that you want to search for
    street_name = name_of_street
    city = "Boston"
    state = "MA"

    # Construct the API request URL
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={api_key}&location={street_name},+{city},+{state}"

    # Send the request to the API and get the response
    response = requests.get(url)
    data = response.json()

    start_address = data['results'][0]['locations'][0]['latLng']['lng']
    end_address = data['results'][0]['locations'][0]['latLng']['lat']

    print(start_address, end_address)
    print(data)


# Waypoint format should be like the following: "1 Huntington Ave, Boston, MA 02116"
# Waypoints MUST BE in ascending/descending order according to origin/destination
def waypoints_to_string(list_of_waypoints):
    result = ""

    for address in list_of_waypoints:
        plus_replace_space = address.replace(" ", "+")
        result += "via:" + plus_replace_space + "|"

    return result


def polyline_demo():
    origin = '3700 Huntington Avenue, Boston, MA 02116'
    destination = '1 Huntington Avenue, Boston, MA 02116'
    waypoints = 'via:3000+Huntington+Avenue,+Boston,+MA|' \
                'via:2000+Huntington+Avenue,+Boston,+MA|' \
                'via:1000+Huntington+Avenue,+Boston,+MA|'

    waypoints = waypoints_to_string(["3000 Huntington Ave, Boston, MA 02116",
                                     "2000 Huntington Ave, Boston, MA 02116",
                                     "1000 Huntington Ave, Boston, MA 02116"])

    response = requests.get(
        f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}'
        f'&waypoints={waypoints}&key={API_KEY_GOOGLE}')

    polyline_string = response.json()['routes'][0]['overview_polyline']['points']

    points = polyline.decode(polyline_string)
    print('points')
    for point in points:
        print(point)


if __name__ == '__main__':
    # start_lat, start_lng, end_lat, end_lng = get_street_bounds(street_name)
    # start_lat, start_lng, end_lat, end_lng = 42.3306292, -71.1151431, 42.3511992, -71.0765188
    # print(str(start_lat) + ", " + str(start_lng))
    # print(str(end_lat) + ", " + str(end_lng))

    # polyline_demo()
    # map_quest_get_bounds(street_name)
    pass

