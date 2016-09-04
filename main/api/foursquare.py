import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime
import time

FOURSQUARE_API_URL = 'https://api.foursquare.com/v2/'

def refresh_checkin_history(user):
    # TODO
    print 'FOURSQUARE REQUEST'

    # Query parameters
    after_timestamp = 1262304000
    before_timestamp = time.time()
    limit = 250
    sort = 'oldestfirst'

    more_to_parse = True

    while more_to_parse:
        more_to_parse = False

        url_to_get = FOURSQUARE_API_URL + 'users/self/checkins?' + 'limit=' + str(limit) + '&sort=' + sort + '&afterTimestamp=' + str(after_timestamp) + '&beforeTimestamp' + str(before_timestamp) + '&oauth_token=' + user.foursquareconnection.access_token + '&m=swarm' + '&v=20160904' 

        print '################# MAKING REQUEST ####################'
        print url_to_get
        print '#####################################################'

        r = requests.get(url_to_get)

        checkins_json = r.json()

        checkin_count = checkins_json['response']['checkins']['count']
        checkin_items = checkins_json['response']['checkins']['items']

        

        print checkins_json