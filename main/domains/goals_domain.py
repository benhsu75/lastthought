from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_goals(current_user, text):
    # Log response
    message_log.log_message('goals_trigger_response', current_user, text, None)

    fbid = current_user.fbid
    
    # Send message
    if 'goals' in text:
        goals_trigger_message = "Manage your goals:"
        send_api_helper.send_button_message(fbid, goals_trigger_message, [
                    {
                        'type': 'web_url',
                        'url': BASE_HEROKU_URL + '/users/'+fbid+'/goals',
                        'title': 'See Goals'    
                    },
                    {
                        'type': 'web_url',
                        'url': BASE_HEROKU_URL + '/users/'+fbid+'/add_goal',
                        'title': 'Add Goal'    
                    }
                ])
        message_log.log_message('goals_trigger_message', current_user, goals_trigger_message, None)