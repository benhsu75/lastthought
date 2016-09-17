import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime
import time

FOURSQUARE_API_URL = 'https://api.foursquare.com/v2/'

def refresh_checkin_history(user):

    # Query parameters
    after_timestamp = 1262304000
    limit = 250
    sort = 'oldestfirst'

    more_to_parse = True

    while more_to_parse:
        user_log = Log.find_or_create(user)
        more_to_parse = False

        url_to_get = FOURSQUARE_API_URL + 'users/self/checkins?' + 'limit=' + str(limit) + '&sort=' + sort + '&afterTimestamp=' + str(after_timestamp) + '&oauth_token=' + user.foursquareconnection.access_token + '&m=swarm' + '&v=20160904' 

        print '################# MAKING REQUEST ####################'
        print url_to_get
        print '#####################################################'

        r = requests.get(url_to_get)

        checkins_json = r.json()

        checkin_count = checkins_json['response']['checkins']['count']

        checkin_items = checkins_json['response']['checkins']['items']

        # Set will continue flag
        if checkin_count > 0 and len(checkin_items) == 250:
            more_to_parse = True

        # Look through checkins
        count = 0
        print 'LENGTH of checkin items: ' + str(len(checkin_items))
        for checkin in checkin_items:
            count += 1

            # Check for venue log entry with the same id
            try:
                venue_log_entry = VenueLogEntry.objects.get(foursquare_id=checkin['id'])
            except VenueLogEntry.DoesNotExist:
                # Create venue log entry
                venue_log_entry = VenueLogEntry(source_type=0)

                venue_log_entry.occurred_at = datetime.datetime.fromtimestamp(checkin['createdAt'])
                venue_log_entry.log = user_log
                venue_log_entry.entry_type = 4

                venue_log_entry.foursquare_id = checkin['id']

                venue_log_entry.lat = checkin['venue']['location']['lat']
                venue_log_entry.lng = checkin['venue']['location']['lng']
                venue_log_entry.formatted_address = checkin['venue']['location']['formattedAddress'][0]
                venue_log_entry.name = checkin['venue']['name']
                if 'shout' in checkin:
                    venue_log_entry.comment = checkin['shout']

                # Todo image url
                if checkin['photos']['count'] > 0:
                    venue_log_entry.img_dim_width = checkin['photos']['items'][0]['width']
                    venue_log_entry.img_dim_height = checkin['photos']['items'][0]['height']

                    venue_log_entry.img_url_prefix = checkin['photos']['items'][0]['prefix']
                    venue_log_entry.img_url_prefix = checkin['photos']['items'][0]['suffix']

                venue_log_entry.save()

            # Change after_timestamp to iterate
            print 'COUNT: ' + str(count)
            print 'Checking Count: ' + str(checkin_count)
            if count == checkin_count or count == 250:
                after_timestamp = checkin['createdAt'] + 1







