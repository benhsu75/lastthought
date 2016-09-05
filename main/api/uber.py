import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

OAUTH_URL = 'https://login.uber.com/oauth/v2/token'

def refresh_ride_history(user):
    x = 1

def refresh_bearer_token(user):
    print 'IN REFRESH BEARER TOKEN'
    # Get refresh token
    refresh_token = current_user.uberconnection.refresh_token

    # Make request to get access_token
    payload = {
        'client_id' : constants.UBER_CLIENT_ID,
        'client_secret' : constants.UBER_CLIENT_SECRET
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token,
        'redirect_uri' : 'https://userdatagraph.herokuapp.com/uber_redirect'
    }

    r = requests.post(OAUTH_URL, data=payload);

    print r.json()

    bearer_token = r.json()['access_token']

    # Update refresh_token
    user.uberconnection.refresh_token = r.json()['refresh_token']

    return bearer_token