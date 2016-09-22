from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper

def handle_misunderstood(current_profile, text, processed_text):
    # Log response
    message_log.log_message('misunderstood_response', current_profile, text, None)

    fbid = current_profile.fbid
    
    misunderstood_message = "Sorry, I don't understand."
    send_api_helper.send_basic_text_message(fbid, misunderstood_message)
    message_log.log_message('misunderstood_message', current_profile, misunderstood_message, None)