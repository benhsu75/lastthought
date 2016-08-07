from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *

def handle(current_user, text, processed_text):
    # Log response from user
    message_log.log_message('help_response', current_user, text, None)

    # Send learn more message
    send_learn_more_message(current_user.fbid)

def send_learn_more_message(fbid):
    learn_more_message = "To learn more about everything I can help you with, click Learn More!"
    send_api_helper.send_button_message(fbid, learn_more_message, [
            {
                'type': 'web_url',
                'url': 'http://userdatagraph.herokuapp.com/learn_more',
                'title': 'Learn More'    
            }
        ])
    message_log.log_message('learn_more_message', current_user, learn_more_message, None)