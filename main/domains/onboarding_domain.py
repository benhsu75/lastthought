from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper, fb_profile_helper
from main.models import *

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def create_new_user(fbid):
    # If user doesn't exist, create user
    u = User(fbid=fbid)
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
    welcome_message = "Hey "+ first_name +"! Nice to meet you. I'm Jarvis, here to help you keep a diary of your life!"
    send_api_helper.send_basic_text_message(fbid, welcome_message)
    message_log.log_message('welcome_message', u, welcome_message, None)

    # Send "Learn More"
    send_learn_more_message(u)

def send_learn_more_message(current_user):
    learn_more_message = "It's super simple - anytime you want to remember something, whether it be a thought, photo, or video, simply send it to me and I'll store it for you!"
    send_api_helper.send_button_message(current_user.fbid, learn_more_message, [
            {
                'type': 'web_url',
                'url': 'http://userdatagraph.herokuapp.com/learn_more',
                'title': 'Learn More'    
            }
        ])
    message_log.log_message('learn_more_message', current_user, learn_more_message, None)