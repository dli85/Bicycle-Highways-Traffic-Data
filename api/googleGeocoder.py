import os
from dotenv import load_dotenv
import googlemaps
import requests

load_dotenv("api.env")
API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE_MAPS')
API_KEY_MAP_QUEST = os.getenv('API_KEY_MAP_QUEST')

street_name = "Huntington Avenue, Boston, MA"
gmaps = googlemaps.Client(key=API_KEY_GOOGLE)


def get_street_bounds(name_of_street):
    geocode_result = gmaps.geocode(name_of_street)

    endpoint_1 = geocode_result[0]['geometry']['location']
    endpoint_2 = geocode_result[0]['geometry']['viewport']

    print(f"Endpoint 1: {endpoint_1['lat']}, {endpoint_1['lng']}")
    print(f"Endpoint 2: {endpoint_2['northeast']['lat']}, {endpoint_2['northeast']['lng']}")
    print(f"Endpoint 3: {endpoint_2['southwest']['lat']}, {endpoint_2['southwest']['lng']}")

    return endpoint_2['southwest']['lat'], endpoint_2['southwest']['lng'], \
        endpoint_2['northeast']['lat'], endpoint_2['northeast']['lng'],



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


# Distance matrix with one origin and one destination
def get_distance_matrix(start_latitude, start_longitude, end_latitude, end_longitude):
    city = "Boston"
    state = "MA"
    geocode_result = gmaps.geocode(f"{street_name}, {city}, {state}")

    # start_address = geocode_result[0]['geometry']['bounds']['southwest']['formatted_address']
    # end_address = geocode_result[0]['geometry']['bounds']['northeast']['formatted_address']

    # print(f"Start address: {start_address}")
    # print(f"End address: {end_address}")

    print(geocode_result)


if __name__ == '__main__':
    start_lat, start_lng, end_lat, end_lng = get_street_bounds(street_name)
    # start_lat, start_lng, end_lat, end_lng = 42.3306292, -71.1151431, 42.3511992, -71.0765188
    # print(str(start_lat) + ", " + str(start_lng))
    # print(str(end_lat) + ", " + str(end_lng))

    # get_distance_matrix(start_lat, start_lng, end_lat, end_lng)

    # map_quest_get_bounds(street_name)

