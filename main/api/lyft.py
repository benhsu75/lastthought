import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

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
    refresh_token = current_user.lyftconnection.refresh_token

    # Make request to get access_token
    payload = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token
    }

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.LYFT_CLIENT_ID, constants.LYFT_CLIENT_SECRET));

    bearer_token = r.json()['access_token']

    return bearer_token
    
#############################################################
################### PUBLIC SCOPE METHODS ####################
#############################################################

def get_eta(lat, lng):
    # Get access_tokenmodels.CharField(max_length=500, null=True)
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
    user_log = Log.find_or_create(current_user)

    # Get bearer token
    bearer_token = refresh_bearer_token(current_user)

    # Make request to /ride
    headers = {
        'Authorization' : 'Bearer ' + bearer_token
    }

    # Query parameters
    start_time = '2015-01-01T00:00:00Z'
    current_time = datetime.date.today().strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = current_time
    limit = 50
    more_to_parse = True

    while more_to_parse:
        more_to_parse = False

        url_to_get = RIDES_URL + '?start_time=' + start_time + '&end_time=' + end_time + '&limit=' + str(limit)
        print '################# MAKING REQUEST ####################'
        print url_to_get
        print '#####################################################'

        r = requests.get(url_to_get, headers=headers)

        ride_history = r.json()['ride_history']

        # Loop through all rides

        count = 0
        for ride in ride_history:
            more_to_parse = True
            count += 1

            requested_at = ride['requested_at']
            raw_time_of_last_ride = requested_at[0:(len(requested_at)-6)]
            requested_at_date = datetime.datetime.strptime(raw_time_of_last_ride, '%Y-%m-%dT%H:%M:%S')

            if count == len(ride_history):
                
                new_date = requested_at_date + datetime.timedelta(seconds=1)
                start_time = new_date.strftime("%Y-%m-%dT%H:%M:%SZ")

            print '--------RIDE--------'
            print ride
            print '--------------------'
            print '\n'

            ride_id = ride['ride_id']

            # Check if ride already in db
            existing_ride = RideLogEntry.objects.filter(ride_id=ride_id, rideshare_service=0)
            if len(existing_ride) != 0:
                print 'RIDE ALREADY IN DB'
                continue

            status = ride['status']
            ride_type = ride['ride_type']
            pax_first_name = ride['passenger']['first_name']

            if status == 'canceled':
                print 'THIS RIDE WAS CANCELLED - NOT STORING'
                # Do something
                x = 1
            else:
                driver_first_name = ride['driver']['first_name']
                driver_rating = ride['driver']['rating']

                #
                ride_entry = RideLogEntry(requested_at=requested_at_date, occurred_at=requested_at_date,ride_id=ride_id, ride_type=ride_type, status=status, driver_first_name=driver_first_name, log=user_log, entry_type=3,rideshare_service=0)

                # Origin
                ride_entry.origin_lat = ride['origin']['lat']
                ride_entry.origin_lng = ride['origin']['lng']
                ride_entry.origin_address = ride['origin']['address']

                
                # Destination
                if 'destination' in ride:
                    ride_entry.dest_lat = ride['destination']['lat']
                    ride_entry.dest_lng = ride['destination']['lng']
                    ride_entry.dest_address = ride['destination']['address']
                    # destination_eta_seconds = ride['destination']['eta_seconds']

                # Pickup
                if 'pickup' in ride:
                    ride_entry.pickup_lat = ride['pickup']['lat']
                    ride_entry.pickup_lng = ride['pickup']['lng']
                    ride_entry.pickup_address = ride['pickup']['address']

                    raw_pickup_time = ride['pickup']['time']

                # Dropoff 
                if 'dropoff' in ride:
                    ride_entry.dropoff_lat = ride['dropoff']['lat']
                    ride_entry.dropoff_lng = ride['dropoff']['lng']
                    ride_entry.dropoff_address = ride['dropoff']['address']

                    raw_dropoff_time = ride['dropoff']['time']

                # # Location
                # if 'location' in ride:
                #     ride_entry.location_lat = ride['location']['lat']
                #     ride_entry.location_lng = ride['location']['lng']
                #     ride_entry.location_address = ride['location']['address']

                if 'primetime_percentage' in ride:
                    ride_entry.primetime_percentage = int(ride['primetime_percentage'].replace('%', ''))
                else:
                    ride_entry.primetime_percentage = 0

                ride_entry.price_in_dollars = ride['price']['amount']/100.0

                ride_entry.save()
                print "SAVED RIDE ENTRY"


