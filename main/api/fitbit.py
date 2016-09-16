import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

def refresh_bearer_token(user):
    # Get refresh token
    refresh_token = user.fitbitconnection.refresh_token

    # Make request to get access_token
    payload = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token
    }

    OAUTH_URL = 'https://api.fitbit.com/oauth2/token'

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.FITBIT_CLIENT_ID, constants.FITBIT_CLIENT_SECRET));

    print r.text

    bearer_token = r.json()['access_token']

    return bearer_token

def refresh_weight_history(user):
    # Get the access token
    access_token = refresh_bearer_token(user)

    # Make request
    user_log = Log.find_or_create(user)
    
    # Make request to /ride
    headers = {
        'Authorization' : 'Bearer ' + access_token
    }

    # Loop through requests to get weight
    more_to_parse = True
    base_year = 2010
    base_month = 1
    base_day = '01'
    base_date_string = '2010-01-01'
    period = '1m'
    url_to_get = 'https://api.fitbit.com/1/user/{}/body/log/weight/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, base_date_string, period)

    while more_to_parse:
        r = requests.ge(url_to_get, headers=headers)

        if 'weight' in r.json():
            weight_list = r.json()['weight']

            for weight_log in weight_list:
                date = weight_log['date']
                time = weight_log['time']
                logId = weight_log['logId']
                metric_weight = weight_log['metric_weight']
                source = weight_log['source']

                weight_log_entry = WeightLogEntry.objects.get(log=user_log, )

        else:
            # ERROR
            # TODO
            x = 1

        # Get current year


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