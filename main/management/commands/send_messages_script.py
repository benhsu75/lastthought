from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main import messenger_helper
from datetime import datetime

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("SENDING MESSAGES")
        # Get current UTC hour
        current_datetime = datetime.utcnow()
        current_utc_hour = current_datetime.hour
        print('Current UTC: ' + str(current_utc_hour))

        # Filter
        all_goals_at_current_time = Goal.objects.all().filter(send_time_utc=current_utc_hour)

        print(len(all_goals_at_current_time))

        # Send messages
        for g in all_goals_at_current_time:
            user = g.user
            fbid = user.fbid

            # Message format depends on the response type
            if(g.response_type == 0): # Numeric response
                messenger_helper.send_basic_text_message(fbid, g.send_text)
            elif(g.response_type == 1): # Binary response
                # Construct button_list
                button_list = []
                button_list.append({
                        'type': 'postback',
                        'title': 'Yes',
                        'payload': '1'
                    })
                button_list.append({
                        'type': 'postback',
                        'title': 'No',
                        'payload': '0'
                    })

                messenger_helper.send_button_message(fbid, g.send_text, button_list)
            elif(g.response_type == 2):
                # Text response
                messenger_helper.send_basic_text_message(fbid, g.send_text)
            elif(g.response_type == 3):
                # File response
                messenger_helper.send_basic_text_message(fbid, g.send_text)

            # Create GoalEntry
            goal_entry = GoalEntry(goal=g)
            goal_entry.save()

            user.active_goal_entry = goal_entry
            user.save()