from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_onboard_flow(current_user, fbid, text):
    if(current_user.state == 0):
        # Parse out name from text
        name = text
        name_tokenized = name.split(' ')
        first_name = name_tokenized[0]

        # Update user
        current_user.full_name = name
        current_user.first_name = first_name
        current_user.save()

        # Send message about how to use
        nice_to_meet_message = "Nice to meet you, " + first_name + "! I'm here to make it easier for you to do things. I can help you track reminders, set goals, and more."
        send_api_helper.send_basic_text_message(fbid, nice_to_meet_message)
        message_log.log_message('nice_to_meet_message', current_user, nice_to_meet_message, None)

        learn_more_message = "To learn more about everything I can help you with, click Learn More!"
        send_api_helper.send_button_message(fbid, learn_more_message, [
                {
                    'type': 'web_url',
                    'url': 'http://userdatagraph.herokuapp.com/learn_more',
                    'title': 'Learn More'    
                }
            ])
        message_log.log_message('learn_more_message', current_user, learn_more_message, None)

        # Update user state
        current_user.state = 1
        current_user.save()

    else:
        return