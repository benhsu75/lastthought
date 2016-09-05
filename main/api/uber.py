import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

def refresh_ride_history(user):
    x = 1

def refresh_bearer_token(user):
    # Get refresh token
    refresh_token = current_user.uberconnection.refresh_token

    # Make request to get access_token
    payload = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token
    }

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.LYFT_CLIENT_ID, constants.LYFT_CLIENT_SECRET));

    bearer_token = r.json()['access_token']

    return bearer_token