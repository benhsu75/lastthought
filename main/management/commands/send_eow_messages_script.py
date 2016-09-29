from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.entrypoints.messenger import send_api_helper
from datetime import datetime, timedelta
from main.message_log import message_log
from main.utils import constants

def send_num_thoughts_helper(num_thoughts, profile):
    weekly_message = (
            "You stored {} thoughts last week - tap the link below to view them!".format(num_thoughts)
        )
    send_api_helper.send_button_message(profile.fbid, weekly_message, [
        {
            'type': 'web_url',
            'url': constants.BASE_HEROKU_URL,
            'title': 'View Thoughts'    
        }
    ])
    message_log.log_message(
        'weekly_message',
        profile,
        weekly_message,
        None
    )

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # Get current UTC hour
        current_datetime = datetime.utcnow()
        week_delta = timedelta(days=7)
        one_week_ago_datetime = current_datetime - week_delta

        # Loop through all users
        all_profiles = Profile.objects.all()

        for profile in all_profiles:
            # TEMP (FOR TESTING)
            if profile.id != 24:
                continue

            # Ensure user hasn't disabled the weekly reminder
            if not profile.send_reminders_flag:
                continue

            # Find out how many thoughts the user has logged in the past week
            user_log = Log.find_or_create(profile)
            last_week_logs = LogEntry.objects.filter(
                log=user_log,
                occurred_at__gt=one_week_ago_datetime
                )
            # TODO
            num_thoughts_this_week = len(last_week_logs)

            # Send user message with link to view logs (in batch)
            send_num_thoughts_helper(num_thoughts_this_week, profile)

    

        