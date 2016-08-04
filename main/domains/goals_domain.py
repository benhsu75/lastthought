from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_goals(current_user, text):
    if 'goals' in text:
        send_api_helper.send_button_message(fbid, "Manage your goals:", [
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