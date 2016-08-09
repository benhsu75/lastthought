from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import constants

def handle(current_user, text, processed_text):
    # Log ride response
    message_log.log_message('ridesharing_setup_response', current_user, text, None)

    # Send the ridesharing message and url
    ridesharing_setup_message = "Setup ridesharing:"
    send_api_helper.send_button_message(current_user.fbid, ridesharing_setup_message, [{
            'type': 'web_url',
            'url': constants.BASE_HEROKU_URL + '/users/'+str(current_user.fbid)+'/setup_ridesharing',
            'title': 'Go'
        }])
    message_log.log_message('ridesharing_setup_message', current_user, ridesharing_setup_message, None)
    
def lyft_webhook(request):
    # Todo
    x = 1

    print request.GET

def uber_webhook(request):
    # Todo
    x = 1
