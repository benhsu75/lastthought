import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

OAUTH_URL = 'https://login.uber.com/oauth/v2/token'
BASE_URL = 'https://api.uber.com'

def refresh_ride_history(user):
    print '--------GETTING RIDE HISTORY----------'

    user_log = Log.find_or_create(user)

    bearer_token = refresh_bearer_token(user)

    # Make request to get ride history
    ride_history_url = BASE_URL + '/v1.2/history'

    offset = 0
    headers = {
        "Authorization" : "Bearer " + bearer_token
    }
    url_to_get = ride_history_url + '?limit=50&offset={}'.format(offset)
    more_to_parse = True

    product_mapping = {} # key = id, value = name

    while more_to_parse:
        r = requests.get(url_to_get, headers=headers)
        # print r.json()

        count = r.json()['count']
        if offset < count:
            more_to_parse = True
            offset += 50
        else:
            more_to_parse = False

        history = r.json()['history']

        for ride in history:
            request_id = ride['request_id']
            product_id = ride['product_id']
            distance = ride['distance']
            request_time = ride['request_time']
            start_time = ride['start_time']
            end_time = ride['end_time']
            start_city_name = ride['start_city']['display_name']
            start_city_lat = ride['start_city']['latitude']
            start_city_lng = ride['start_city']['longitude']

            request_datetime = datetime.datetime.fromtimestamp(request_time)
            start_datetime = datetime.datetime.fromtimestamp(start_time)
            end_datetime = datetime.datetime.fromtimestamp(end_time)

            if product_id not in product_mapping:
                product_response = get_product_info(bearer_token, product_id)

                product_name = product_response['display_name']
                product_mapping[product_id] = product_name
            
            product_display_name = product_mapping[product_id]

            # Create ridelogentry object

            # Check if ride already in db
            try:
                ride_log_entry = RideLogEntry.objects.get(ride_id=request_id)
                print 'RIDE ALREADY EXISTS'
            except RideLogEntry.DoesNotExist:
                print 'CREATING NEW RIDE LOG ENTRY'
                ride_log_entry = RideLogEntry(occurred_at=start_datetime, log=user_log, entry_type=3, requested_at=request_datetime)

                ride_log_entry.rideshare_service = 1
                ride_log_entry.ride_id = request_id
                ride_log_entry.ride_type = product_display_name
                ride_log_entry.distance = distance
                ride_log_entry.start_time = start_datetime
                ride_log_entry.end_time = end_datetime
                ride_log_entry.start_city_name = start_city_name
                ride_log_entry.start_city_lat = start_city_lat
                ride_log_entry.start_city_lng = start_city_lng

                ride_log_entry.save()

    x = 1

def refresh_bearer_token(user):
    print 'IN REFRESH BEARER TOKEN'
    # Get refresh token
    refresh_token = user.uberconnection.refresh_token

    print 'USING REFRESH TOKEN: ' + refresh_token

    # Make request to get access_token
    payload = {
        'client_id' : constants.UBER_CLIENT_ID,
        'client_secret' : constants.UBER_CLIENT_SECRET,
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token,
        'redirect_uri' : 'https://userdatagraph.herokuapp.com/uber_redirect/'
    }

    r = requests.post(OAUTH_URL, data=payload);

    print r.json()

    bearer_token = r.json()['access_token']

    # Update refresh_token
    user.uberconnection.refresh_token = r.json()['refresh_token']
    print 'NEW REFRESH TOKEN: ' + user.uberconnection.refresh_token
    user.uberconnection.save()

    return bearer_token

def get_ride_info(bearer_token, request_id):
    print '-------------GETTING RIDE INFO-------'
    print 'BEARER: '  + bearer_token
    print 'request id: ' + request_id
    ride_url = BASE_URL + '/v1/requests/' + request_id

    headers = {
        "Authorization" : "Bearer " + bearer_token
    }

    url_to_get = ride_url
    r = requests.get(url_to_get, headers=headers)

    print r.json()

def get_product_info(bearer_token, product_id):
    print ''
    print "GETTING PRODUCT INFO!!!!"
    print ''
    product_url = BASE_URL + '/v1/products/' + product_id

    headers = {
        "Authorization" : "Bearer " + bearer_token
    }

    url_to_get = product_url
    r = requests.get(url_to_get, headers=headers)

    return r.json()

