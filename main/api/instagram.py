import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

BASE_URL = 'https://api.instagram.com/v1'

def refresh_instagram_history(user):
    print '--------GETTING INSTAGRAM HISTORY----------'

    user_log = Log.find_or_create(user)

    access_token = user.instagramconnection.access_token

    # Make request to get all media
    recent_media_url = BASE_URL + '/users/self/media/recent/'

    # Add access token and count to url
    url_to_get = recent_media_url + '?access_token=' + access_token + '&count=20'

    more_to_parse = True

    while more_to_parse:
        more_to_parse = False
        print "Requesting: " + url_to_get

        r = requests.get(url_to_get)

        if r.json()['meta']['code'] != 200:
            # Handle error
            return

        # Parse data into log entries

        # More to parse if data in pagination
        if 'next_url' in r.json()['pagination']:
            more_to_parse = True
            url_to_get = r.json()['pagination']['next_url']

        # Retrieve data
        media_list = r.json()['data']

        for media in media_list:

            # Extract all the information
            media_type = media['type']

            if media_type == 'image': # Media was image
                if media['location'] != None:
                    location_lat = media['location']['latitude']
                    location_lng = media['location']['longitude']
                    location_name = media['location']['name']

                num_comments = media['comments']['count']

                created_time = float(media['created_time'])
                created_datetime = datetime.datetime.fromtimestamp(created_time)

                link_to_post = media['link']

                num_likes = media['likes']['count']

                thumbnail_url = media['images']['thumbnail']['url']
                thumbnail_height = media['images']['thumbnail']['height']
                thumbnail_width = media['images']['thumbnail']['width']

                low_res_url = media['images']['low_resolution']['url']
                low_res_height = media['images']['low_resolution']['height']
                low_res_width = media['images']['low_resolution']['width']

                high_res_url = media['images']['standard_resolution']['url']
                high_res_height = media['images']['standard_resolution']['height']
                high_res_width = media['images']['standard_resolution']['width']

                caption = media['caption']['text']

                instagram_id = media['id']

                # Create InstagramLogEntry

                # Check if one with this id already exists
                try:
                    instagram_log_entry = InstagramLogEntry.objects.get(instagram_id=instagram_id)
                except InstagramLogEntry.DoesNotExist:
                    print 'Creating new InstagramLogEntry'
                    instagram_log_entry = InstagramLogEntry(occurred_at=created_datetime, log=user_log, entry_type=5)

                    instagram_log_entry.instagram_id = instagram_id
                    instagram_log_entry.likes = num_likes
                    instagram_log_entry.link_to_post = link_to_post

                    instagram_log_entry.thumbnail_url = thumbnail_url
                    instagram_log_entry.thumbnail_height = thumbnail_height
                    instagram_log_entry.thumbnail_width = thumbnail_width

                    instagram_log_entry.low_res_url = low_res_url
                    instagram_log_entry.low_res_height = low_res_height
                    instagram_log_entry.low_res_width = low_res_width

                    instagram_log_entry.high_res_url = high_res_url
                    instagram_log_entry.high_res_height = high_res_height
                    instagram_log_entry.high_res_width = high_res_width

                    if media['location'] != None:
                        instagram_log_entry.lat = location_lat
                        instagram_log_entry.lng = location_lng
                        instagram_log_entry.location_name = location_name

                    instagram_log_entry.caption = caption

                    instagram_log_entry.save()
            elif media_type == 'video':
                # TODO
                x = 1















