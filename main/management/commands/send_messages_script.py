from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.entrypoints.messenger import send_api_helper
from datetime import datetime
from main.message_log import message_log

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
                send_api_helper.send_basic_text_message(fbid, g.send_text)
                message_log.log_message('goal_prompt_message', user, g.send_text, {'goal': g})
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

                send_api_helper.send_button_message(fbid, g.send_text, button_list)
                message_log.log_message('goal_prompt_message', user, g.send_text, {'goal': g})
            elif(g.response_type == 2):
                # Text response
                send_api_helper.send_basic_text_message(fbid, g.send_text)
                message_log.log_message('goal_prompt_message', user, g.send_text, {'goal': g})
            elif(g.response_type == 3):
                # File response
                send_api_helper.send_basic_text_message(fbid, g.send_text)
                message_log.log_message('goal_prompt_message', user, g.send_text, {'goal': g})

            # Create GoalEntry
            goal_entry = GoalEntry(goal=g)
            goal_entry.save()

            user.active_goal_entry = goal_entry
            user.save()