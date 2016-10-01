from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.entrypoints.messenger import send_api_helper
from datetime import datetime, timedelta
from main.message_log import message_log
from main.utils import constants


def send_num_thoughts_helper(num_thoughts, profile, time_period):
    weekly_message = (
        "You stored {} thoughts {} - tap the link below to view them!".format(num_thoughts, time_period)
    )
    send_api_helper.send_button_message(profile.fbid, weekly_message, [
        {
            'type': 'web_url',
            'url': constants.BASE_HEROKU_URL,
            'title': 'View Thoughts',
            "messenger_extensions": True
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
        day_delta = timedelta(days=1)
        one_day_ago_datetime = current_datetime - day_delta

        # Loop through all users
        all_profiles = Profile.objects.all()

        for profile in all_profiles:
            # TEMP (FOR TESTING) - just send to ben and cathy
            if profile.id != 24 and profile.id != 25:
                continue

            # Ensure user hasn't disabled the weekly reminder
            if not profile.send_reminders_flag:
                continue

            # Find out how many thoughts the user has logged in the past day
            user_log = Log.find_or_create(profile)
            last_day_logs = LogEntry.objects.filter(
                log=user_log,
                occurred_at__gt=one_day_ago_datetime
            )
            # TODO
            num_thoughts_this_day = len(last_day_logs)

            if num_thoughts_this_day > 0:
                # Send the view message to the user
                send_num_thoughts_helper(num_thoughts_this_day, profile, 'today')
                continue

            # Look at users reminder_settings field
            if profile.reminder_settings == 0: # Always send daily
                # Send the view message to the user
                send_num_thoughts_helper(num_thoughts_this_day, profile, 'today')
                continue
            elif profile.reminder_settings == 1:
                # Send the summary if it is Sunday
                if current_datetime.weekday() == 7:
                    # Count how many thoughts the user had in the past week
                    week_delta = timedelta(days=7)
                    one_week_ago_datetime = current_datetime - week_delta

                    last_week_logs = LogEntry.objects.filter(
                        log=user_log,
                        occurred_at__gt=one_week_ago_datetime
                    )
                    num_thoughts_this_week = len(last_week_logs)

                    send_num_thoughts_helper(num_thoughts_this_week, profile, 'last week')
                    continue
            elif profile.reminder_settings == 2:
                # do nothing since user has elected to not receive notifications
                continue
            else:
                continue
            
