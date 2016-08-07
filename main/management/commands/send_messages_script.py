from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.entrypoints.messenger import send_api_helper
from datetime import datetime
from main.message_log import message_log
import json

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # Get current UTC hour
        current_datetime = datetime.utcnow()
        current_utc_hour = current_datetime.hour

        # Filter habits to send now
        all_habits_at_current_time = Habit.objects.all().filter(send_time_utc=current_utc_hour)

        # Send messages
        for h in all_habits_at_current_time:
            user = h.user
            fbid = user.fbid

            # Create HabitEntry
            habit_entry = HabitEntry(habit=h)
            habit_entry.save()

            # Message format depends on the response type
            if h.response_type == 0: # Numeric response
                send_api_helper.send_basic_text_message(fbid, h.send_text)
                message_log.log_message('habit_prompt_message', user, h.send_text, {'habit_entry': habit_entry})
            elif h.response_type == 1: # Binary response
                # Construct button_list
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
            elif h.response_type == 2:
                # Text response

                # Send message and log
                send_api_helper.send_basic_text_message(fbid, h.send_text)
                message_log.log_message('habit_prompt_message', user, h.send_text, {'habit_entry': habit_entry})
            elif h.response_type == 3:
                # File response

                # Send message and log
                send_api_helper.send_basic_text_message(fbid, h.send_text)
                message_log.log_message('habit_prompt_message', user, h.send_text, {'habit_entry': habit_entry})