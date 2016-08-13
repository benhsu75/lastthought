import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth

OAUTH_URL = 'https://api.lyft.com/oauth/token'

# Get's the access_token for public scope requests
def get_access_token():
    # Construct payload
    payload = {
        'grant_type' : 'client_credentials',
        'scope' : 'public'
    }

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.LYFT_CLIENT_ID, constants.LYFT_CLIENT_SECRET));

    access_token = r.json()['access_token']

    return access_token

# Returns a tuple (bearer_token, refresh_token)
def get_bearer_token_and_refresh_token(code):
    payload = {
        'grant_type' : 'authorization_code',
        'code' : code
    }

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.LYFT_CLIENT_ID, constants.LYFT_CLIENT_SECRET));

    bearer_token = r.json()['access_token']
    refresh_token = r.json()['refresh_token']

    return (bearer_token, refresh_token)
    

# Gets a bearer token using the refresh token
def refresh_bearer_token(current_user):
# Get refresh token
    refresh_token = current_user.rideshareinformation.lyft_refresh_token

    # Make request to get access_token
    payload = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token
    }

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.LYFT_CLIENT_ID, constants.LYFT_CLIENT_SECRET));

    print r.text

    bearer_token = r.json()['access_token']

    return bearer_token
    
def get_eta(lat, long):
    # TODO
    x = 1

def request_ride(start_lat, start_long, end_lat, end_long, ride_type):
    # TODO
    x = 1

def cancel_ride(ride_id):
    # TODO
    x = 1

def refresh_ride_history(current_user):
    # TODO 
    x = 1

