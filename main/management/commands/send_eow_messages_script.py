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

        # Loop through all users
        all_profiles = Profile.objects.all()

        for profile in all_profiles:
            # Ensure user hasn't disabled the weekly reminder
            if not profile.send_reminders_flag:
                continue

            # Find out how many thoughts the user has logged in the past week
            user_log = Log.find_or_create(profile)
            last_week_logs = LogEntry.objects.filter(
                user_log=user_log
                )
            # TODO
            num_thoughts_this_week = len(last_week_logs)

            # Send user message with link to view logs (in batch)
            weekly_message = (
                "You stored {} thoughts last week - tap the link below to view them!".format(num_thoughts_this_week)
            )
            send_api_helper.send_button_message(current_profile.fbid, weekly_message, [
                {
                    'type': 'web_url',
                    'url': constants.BASE_HEROKU_URL,
                    'title': 'View Thoughts'    
                }
            ])
            message_log.log_message(
                'weekly_message',
                current_profile,
                weekly_message,
                None
            )

            # Execute batch send

        