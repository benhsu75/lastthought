from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.entrypoints.messenger import send_api_helper
from datetime import datetime
from main.message_log import message_log
import json
from main.utils import helper_util

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # Get all users who want us to send them the commute button
        rideshare_information_list = RideshareInformation.objects.filter(send_ride_button_flag=True)

        for r in rideshare_information_list:
            fbid = r.user.fbid

            if helper_util.user_exists(fbid):
                current_user = User.objects.get(fbid=fbid)
            else:
                continue

            # Set parameters of ride request
            start_address = r.current_home_address
            end_address = r.current_work_address

            start_lat = r.home_lat
            start_lng = r.home_lng
            end_lat = r.work_lat
            end_lng = r.work_lng

            ride_type = r.ride_type_preference

            # Send message
            ride_request_message = "Click the button to request a ride from " + start_address + " to " + end_address
            ride_request_url = generate_ride_request_url(fbid, start_lat, start_lng, end_lat, end_lng, ride_type)
            send_api_helper.send_button_message(fbid, ride_request_message, [
                    {
                        'type': 'web_url',
                        'url': ride_request_url,
                        'title': 'Request Ride'    
                    }
                ])
            message_log.log_message('ride_request_message', current_user, ride_request_message, None)


# Helper methods

# Generate a ride request url
def generate_ride_request_url(fbid, start_lat, start_lng, end_lat, end_lng, ride_type):
    base_url = 'http://userdatagraph.herokuapp.com/users/' + fbid + '/request_ride?'

    base_url += 'start_lat=' + str(start_lat)
    base_url += '&start_lng=' + str(start_lng)
    base_url += '&end_lat=' + str(end_lat)
    base_url += '&end_lng=' + str(end_lng)
    base_url += '&ride_type=' + ride_type

    return base_url



