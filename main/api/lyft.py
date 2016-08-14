import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth

API_BASE_URL = 'https://api.lyft.com'
OAUTH_URL = API_BASE_URL + '/oauth/token'
ETA_URL = API_BASE_URL + '/v1/eta'
COST_URL = API_BASE_URL + '/v1/cost'
RIDES_URL = API_BASE_URL + '/v1/rides'

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
        'origin.lat' : start_lat,
        'origin.lng' : start_lng,
        'destination.lat' : end_lat,
        'destination.lng' : end_lng
    }

    print payload
    r = requests.post(RIDES_URL, data=payload, headers=headers)

    print r.text
    
    if 'status' not in r.json():
        return False

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
    # Get bearer token
    bearer_token = refresh_bearer_token(current_user)

    # Make request to /ride
    headers = {
        'Authorization' : 'Bearer ' + bearer_token
    }

    # Query parameters
    start_time = '2015-01-01T00:00:00Z'
    end_time = '2016-06-01T00:00:00Z'
    limit = 50

    url_to_get = RIDES_URL + '?start_time=' + start_time + '&end_time=' + end_time + '&limit=' + str(limit)

    print url_to_get
    r = requests.get(url_to_get, headers=headers)

    ride_history = r.json()['ride_history']

    # Loop through all rides
    for ride in ride_history:
        print '--------RIDE--------'
        print ride
        print '--------------------'
        print '\n'

        ride_id = ride['ride_id']
        status = ride['status']
        ride_type = ride['ride_type']
        pax_first_name = ride['passenger']['first_name']

        if status == 'canceled':
            # Do something
            x = 1
        else:
            driver_first_name = ride['driver']['first_name']
            driver_rating = ride['driver']['rating']

            # Origin
            origin_lat = ride['origin']['lat']
            origin_lng = ride['origin']['lng']
            origin_address = ride['origin']['address']
            origin_eta_seconds = ride['origin']['eta_seconds']

            # Destination
            if 'destination' in ride:
                destination_lat = ride['destination']['lat']
                destination_lng = ride['destination']['lng']
                destination_address = ride['destination']['address']
                destination_eta_seconds = ride['destination']['eta_seconds']

            # Pickup
            if 'pickup' in ride:
                pickup_lat = ride['pickup']['lat']
                pickup_lng = ride['pickup']['lng']
                pickup_address = ride['pickup']['address']
                pickup_time = ride['pickup']['time']

            # Dropoff 
            if 'dropoff' in ride:
                dropoff_lat = ride['dropoff']['lat']
                dropoff_lng = ride['dropoff']['lng']
                dropoff_address = ride['dropoff']['address']
                dropoff_time = ride['dropoff']['time']

            # Location
            if 'location' in ride:
                location_lat = ride['location']['lat']
                location_lng = ride['location']['lng']
                location_address = ride['location']['address']

            primetime_percentage = ride['primetime_percentage']
            price = ride['price']['amount']

            eta_seconds = ride['eta_seconds']
            requested_at = ride['requested_at']

    # Parse response and put into database

