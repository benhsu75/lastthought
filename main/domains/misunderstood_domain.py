from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper

def handle_misunderstood(current_user, text):
    fbid = current_user.fbid
    
    send_api_helper.send_basic_text_message(fbid, "Sorry, I don't understand.")