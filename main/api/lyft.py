import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth

API_BASE_URL = 'https://api.lyft.com'
OAUTH_URL = API_BASE_URL + '/oauth/token'
ETA_URL = API_BASE_URL + '/v1/eta'
COST_URL = API_BASE_URL + '/v1/cost'
RIDE_REQUEST_URL = API_BASE_URL + '/v1/rides'

#############################################################
###################### AUTH METHODS #########################
#############################################################

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

    print 'Refresh token:'
    print refresh_token

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.LYFT_CLIENT_ID, constants.LYFT_CLIENT_SECRET));

    print r.text

    bearer_token = r.json()['access_token']

    return bearer_token
    
#############################################################
################### PUBLIC SCOPE METHODS ####################
#############################################################

def get_eta(lat, lng):
    # Get access_token
    access_token = get_access_token()

    # Make request to eta endpoint
    headers = {
        "Authorization" : "Bearer " + access_token
    }
    url_to_get = ETA_URL + '?lat=' + str(lat) + '&lng=' + str(lng)

    r = requests.get(url_to_get, headers=headers)

    response = r.json()

    return response

def get_eta_for_ride_type(lat, lng, ride_type):
    # Get access_token
    access_token = get_access_token()

    # Make request to eta endpoint
    headers = {
        "Authorization" : "Bearer " + access_token
    }
    url_to_get = ETA_URL + '?lat=' + str(lat) + '&lng=' + str(lng) + '&ride_type=' + ride_type

    r = requests.get(url_to_get, headers=headers)

    response = r.json()

    return response

def get_cost(start_lat, start_lng, end_lat, end_lng):
    # Get access_token
    access_token = get_access_token()

    # Make request to eta endpoint
    headers = {
        "Authorization" : "Bearer " + access_token
    }
    url_to_get = COST_URL + '?start_lat=' + str(start_lat) + '&start_lng=' + str(start_lng) + '&end_lat=' + str(end_lat) + '&end_lng=' + str(end_lng)

    r = requests.get(url_to_get, headers=headers)

    response = r.json()

    return response

def get_cost_for_ride_type(start_lat, start_lng, end_lat, end_lng, ride_type):
    # Get access_token
    access_token = get_access_token()

    # Make request to eta endpoint
    headers = {
        "Authorization" : "Bearer " + access_token
    }
    url_to_get = COST_URL + '?start_lat=' + str(start_lat) + '&start_lng=' + str(start_lng) + '&end_lat=' + str(end_lat) + '&end_lng=' + str(end_lng) + '&ride_type=' + ride_type

    r = requests.get(url_to_get, headers=headers)

    response = r.json()

    return response

#############################################################
##################### USER METHODS# #########################
#############################################################

def request_ride(current_user, start_lat, start_lng, end_lat, end_lng, ride_type):
    # Get bearer token
    bearer_token = refresh_bearer_token(current_user)

    # Make request to /ride
    headers = {
        'Authorization' : 'Bearer ' + bearer_token
    }

    payload = {
        'ride_type' : ride_type,
        'origin' : {
            'lat' : start_lat,
            'lng' : start_lng
        },
        'destination' : {
            'lat' : end_lat,
            'lng' : end_lng
        }
    }

    r = requests.post(RIDE_REQUEST_URL, data=payload, headers=headers)

    print r.text
    
    status = r.json()['status']

    # Return whether or not the ride was successfully requested
    if status == 'pending':
        return True
    else:
        return False

def cancel_ride(ride_id):
    # TODO
    x = 1

def refresh_ride_history(current_user):
    # TODO 
    x = 1

