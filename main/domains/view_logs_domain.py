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

# Helper method to send message for user to view logs
def send_view_category_message(current_profile, category):
    # Send user message linking to log
    log_view_message = (
        "Click to view your {} category".format(category.context_name)
    )
    link_to_view_category = constants.BASE_HEROKU_URL + '/categories/' + category.id
    send_api_helper.send_button_message(current_profile.fbid, log_view_message, [
        {
            'type': 'web_url',
            'url': link_to_view_category,
            'title': 'View {}'.format(category.context_name)    
        }
    ])
    message_log.log_message(
        'log_view_message',
        current_profile,
        log_view_message,
        None
    )