from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.utils import helper_util, constants

# Helper method to send message for user to view logs
def send_view_logs_message(current_profile):
    # Send user message linking to log
    log_view_message = (
        "Click to view your thoughts"
    )
    send_api_helper.send_button_message(current_profile.fbid, log_view_message, [
        {
            'type': 'web_url',
            'url': constants.BASE_HEROKU_URL,
            'title': 'View Thoughts'    
        }
    ])
    message_log.log_message(
        'log_view_message',
        current_profile,
        log_view_message,
        None
    )