import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth

OAUTH_URL = 'https://api.lyft.com/oauth/token'

# Returns a tuple (access_token, refresh_token)
def retrieve_access_token(code):
    payload = {
        'grant_type' : 'authorization_code',
        'code' : code
    }

    # post
    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.LYFT_CLIENT_ID, constants.LYFT_CLIENT_SECRET));

    access_token = r.json()['access_token']
    refresh_token = r.json()['refresh_token']

    return (access_token, refresh_token)
    
def get_eta(lat, long):
    # TODO
    x = 1

def request_ride(start_lat, start_long, end_lat, end_long, ride_type):
    # TODO
    x = 1

def cancel_ride(ride_id):
    # TODO
    x = 1

def store_ride_history(current_user):
    # TODO 
    x = 1

