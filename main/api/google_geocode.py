from main.utils import constants
import requests
import json

GEOCODING_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'

def geocode_address(address):
    url_to_get = GEOCODING_API_URL + 'address=' + address + '&key=' + constants.GOOGLE_GEOCODING_API_KEY

    r = requests.get(url_to_get)
    json_response = json.loads(r.text)
    
    first_result = json_response['results'][0]

    # Extract response
    lat = first_result['geometry']['location']['lat']
    lng = first_result['geometry']['location']['lng']
    formatted_address = first_result['formatted_address']

    return (formatted_address, lat, lng)
