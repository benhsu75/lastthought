from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.entrypoints.messenger import send_api_helper
from datetime import datetime
from main.message_log import message_log
import json

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("SENDING MESSAGES")
        # Get current UTC hour
        current_datetime = datetime.utcnow()
        current_utc_hour = current_datetime.hour
        print('Current UTC: ' + str(current_utc_hour))

        # Filter
        all_habits_at_current_time = Habit.objects.all().filter(send_time_utc=current_utc_hour)

        print(len(all_habits_at_current_time))

        # Send messages
        for g in all_habits_at_current_time:
            user = g.user
            fbid = user.fbid

            # Create HabitEntry
            habit_entry = HabitEntry(habit=g)
            habit_entry.save()

            # Message format depends on the response type
            if(g.response_type == 0): # Numeric response
                send_api_helper.send_basic_text_message(fbid, g.send_text)
                message_log.log_message('habit_prompt_message', user, g.send_text, {'habit': g})
            elif(g.response_type == 1): # Binary response
                # Construct button_list
                button_list = []

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

                button_list.append({
                        'type': 'postback',
                        'title': 'Yes',
                        'payload': true_payload
                    })
                button_list.append({
                        'type': 'postback',
                        'title': 'No',
                        'payload': false_payload
                    })

                send_api_helper.send_button_message(fbid, g.send_text, button_list)
                message_log.log_message('habit_prompt_message', user, g.send_text, {'habit': g})
            elif(g.response_type == 2):
                # Text response
                send_api_helper.send_basic_text_message(fbid, g.send_text)
                message_log.log_message('habit_prompt_message', user, g.send_text, {'habit': g})
            elif(g.response_type == 3):
                # File response
                send_api_helper.send_basic_text_message(fbid, g.send_text)
                message_log.log_message('habit_prompt_message', user, g.send_text, {'habit': g})

            

            user.active_habit_entry = habit_entry
            user.save()