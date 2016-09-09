import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

def refresh_bearer_token(user):
    x = 1

def refresh_weight_history(user):
    x = 1

def refresh_activity_history(user):
    # TODO
    x = 1

def get_profile_information(user, access_token):
    url_to_get = 'https://api.fitbit.com/1/user/'+user.fitbitconnection.fitbit_id+'/profile.json'

    r = requests.get(url_to_get)

    print r.text

    return r.json()