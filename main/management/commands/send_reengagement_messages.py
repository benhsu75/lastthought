from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main.entrypoints.messenger import send_api_helper
from datetime import datetime, timedelta
from main.message_log import message_log
from main.utils import constants
import pytz

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Get current UTC hour
        current_datetime = datetime.utcnow().replace(
            tzinfo=pytz.utc
        )

        # Loop through all users
        all_profiles = Profile.objects.all()

        for profile in all_profiles:
            # Determine how many days since sign up
            time_since_signup = current_datetime - profile.created_at
            days_since_signup = time_since_signup.days

            if days_since_signup == 1:
                send_first_engage_message(profile)
            elif days_since_signup == 4:
                send_second_engage_message(profile)
            elif days_since_signup == 7:
                send_third_engage_message(profile)
            elif days_since_signup == 14:
                send_fourth_engage_message(profile)

def send_first_engage_message(profile):
    first_engage_message = 'LastThought is great for keeping track of books to read? What\'s one book you recently heard of that you want to check out?'
    send_api_helper.send_basic_text_message(profile.fbid, first_engage_message)
    message_log.log_message(
        'first_engage_message',
        profile,
        first_engage_message,
        None
    )

def send_second_engage_message(profile):
    second_engage_message = 'You can view your thoughts by tapping the little menu in the bottom left of this chat, or you can go to https://www.lastthought.me!'
    send_api_helper.send_basic_text_message(profile.fbid, second_engage_message)
    message_log.log_message(
        'second_engage_message',
        profile,
        second_engage_message,
        None
    )

def send_third_engage_message(profile):
    third_engage_message = 'Everything that we don\t write down we forget. What\'s something you\'ve been thinking about and how do you feel about it?'
    send_api_helper.send_basic_text_message(profile.fbid, third_engage_message)
    message_log.log_message(
        'third_engage_message',
        profile,
        third_engage_message,
        None
    )

def send_fourth_engage_message(profile):
    fourth_engage_message = 'LastThought is great for keeping track of links. Try sending me a link!'
    send_api_helper.send_basic_text_message(profile.fbid, fourth_engage_message)
    message_log.log_message(
        'fourth_engage_message',
        profile,
        fourth_engage_message,
        None
    )