import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

def refresh_bearer_token(user):
    # Get refresh token
    refresh_token = current_user.fitbitconnection.refresh_token

    # Make request to get access_token
    payload = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token
    }

    OAUTH_URL = 'https://api.fitbit.com/oauth2/token'

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.FITBIT_CLIENT_ID, constants.FITBIT_CLIENT_SECRET));

    bearer_token = r.json()['access_token']

    return bearer_token

def refresh_weight_history(user):
    # Get the access token
    access_token = refresh_bearer_token(user)

    # Make request

def refresh_activity_history(user):
    # TODO
    x = 1

def get_profile_information(user, access_token):
    url_to_get = 'https://api.fitbit.com/1/user/'+user.fitbitconnection.fitbit_id+'/profile.json'

    headers = {
        'Authorization' : 'Bearer ' + access_token
    }

    r = requests.get(url_to_get, headers=headers)

    print r.text

    return r.json()