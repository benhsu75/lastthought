from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.entrypoints.messenger import send_api_helper
from datetime import datetime
from main.message_log import message_log
import json

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # Get all users who want us to send them the commute button
        rideshare_information_list = RideshareInformation.objects.filter(send_ride_button_flag=True)

        for r in rideshare_information_list:
            fbid = r.user.fbid

            # Create message
            quick_reply_list = []

            true_payload = json.dumps({
                    'state' : 'habit_binary_response',
                    'habit_entry_id' : habit_entry.id,
                    'value' : 1
                })
            false_payload = json.dumps({
                    'state' : 'habit_binary_response',
                    'habit_entry_id' : habit_entry.id,
                    'value' : 0
                })

            quick_reply_list.append({
                    'content_type': 'text',
                    'title': 'Yes',
                    'payload': true_payload
                })
            quick_reply_list.append({
                    'content_type': 'text',
                    'title': 'No',
                    'payload': false_payload
                })

            # Send message and log
            send_api_helper.send_quick_reply_message(fbid, h.send_text, quick_reply_list)
            message_log.log_message('habit_prompt_message', user, h.send_text, {'habit_entry': habit_entry})


