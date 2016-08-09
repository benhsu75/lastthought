from main.utils import constants
import requests

GEOCODING_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'

def geocode_address(address):
    url_to_get = GEOCODING_API_URL + 'address=' + address + '&key=' + constants.GOOGLE_GEOCODING_API_KEY

    r = requests.get(url_to_get)

    # Parse response