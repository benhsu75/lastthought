from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper, fb_profile_helper
from main.models import *
import help_domain

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def create_new_user(fbid):
    # If user doesn't exist, create user
    u = User(fbid=fbid, state=0)
    u.save()

    # Get user profile information
    (
        first_name,
        last_name,
        profile_pic,
        locale,
        timezone,
        gender
        ) = fb_profile_helper.get_user_profile_data(fbid)

    # Create background information for user
    background_information = BackgroundInformation(user=u, locale=locale, profile_pic=profile_pic, timezone=timezone, gender=gender)
    background_information.save()

    # Send user intro message
    welcome_message = "Hey "+ first_name +"! Nice to meet you. I'm Jarvis, here to help be your better self :)."
    send_api_helper.send_basic_text_message(fbid, welcome_message)
    message_log.log_message('welcome_message', u, welcome_message, None)

    # Send "Learn More"
    help_domain.send_learn_more_message(u)