import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

OAUTH_URL = 'https://login.uber.com/oauth/v2/token'
BASE_URL = 'https://api.uber.com'

def refresh_ride_history(user):
    print '--------GETTING RIDE HISTORY----------'

    bearer_token = refresh_bearer_token(user)

    # Make request to get ride history
    ride_history_url = BASE_URL + '/v1.2/history'

    offset = 0
    headers = {
        "Authorization" : "Bearer " + bearer_token
    }
    url_to_get = ride_history_url + '?limit=50&offset={}'.format(offset)
    more_to_parse = True

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
            request_time = ride['request_time']
            start_time = ride['start_time']
            end_time = ride['end_time']
            request_id = ride['request_id']
            ride_json = get_ride_info(bearer_token, request_id)
        

    x = 1

def refresh_bearer_token(user):
    print 'IN REFRESH BEARER TOKEN'
    # Get refresh token
    refresh_token = user.uberconnection.refresh_token

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


