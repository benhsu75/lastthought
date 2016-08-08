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

# def handle_onboard_flow(current_user, fbid, text, processed_text):
#     fbid = current_user.fbid
    
#     if(current_user.state == 0):
#         # Parse out name from text
#         name = text
#         name_tokenized = name.split(' ')
#         first_name = name_tokenized[0]

#         # Log response
#         message_log.log_message('name_response', current_user, text, None)

#         # Update user
#         current_user.full_name = name
#         current_user.first_name = first_name
#         current_user.save()

#         # Send message about how to use
#         nice_to_meet_message = "Nice to meet you, " + first_name + "! I'm here to make it easier for you to do things. I can help you track reminders, set habits, and more."
#         send_api_helper.send_basic_text_message(fbid, nice_to_meet_message)
#         message_log.log_message('nice_to_meet_message', current_user, nice_to_meet_message, None)

#         # Send "Learn More"
#         help_domain.send_learn_more_message(current_user)

#         # Update user state
#         current_user.state = 1
#         current_user.save()

#     else:
#         return