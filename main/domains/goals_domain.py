from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import helper_util

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

affirmative_synonyms = [
    'yes',
    'yep',
    'y',
    'ya'
]

negative_synonyms = [
    'no',
    'nope',
    'n',
    'nah'
]

def handle_goals(current_user, text):

    # Get context
    fbid = current_user.fbid
    last_message = Message.objects.filter(user=current_user).order_by('-created_at')[0]
    last_prompt_message = Message.objects.filter(user=current_user, message_type=6).order_by('-created_at')[0]
    
    # Send message
    if 'goals' in text:
        # Log response
        message_log.log_message('goals_trigger_response', current_user, text, None)

        # Send message
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
    elif(last_message.message_type  == 6 or helper_util.same_day(last_prompt_message.created_at, datetime.today())):
        # Triage and store
        goal_in_reference = last_message.goal_in_reference
        goal_entry = GoalEntry.objects.filter(goal=goal_in_reference).order_by('-created_at')[0]

        if(goal_in_reference.response_type == 0): # Numeric
            # Convert to float
            try:
                val = float(text)
            except:
                # Log response
                message_log.log_message('goals_trigger_response', current_user, text, None)
                misunderstood_goal_response(current_user, goal_in_reference.response_type)
                return

            # Log response
            message_log.log_message('goal_prompt_response', current_user, text, None)
            
            # Set the data in goal_entry
            goal_entry.numeric_value = val
            goal_entry.save()

            # Understood!
            understood_goal_response(current_user)

        elif(goal_in_reference.response_type == 1): # Binary
            # Convert text to 0 or 1
            text = text.strip()
            if text in affirmative_synonyms:
                binary_value = 1
            elif text in negative_synonyms:
                binary_value = 0
            else:
                # Log invalid response
                message_log.log_message('goals_trigger_response', current_user, text, None)

                # Send message
                misunderstood_goal_response(current_user, goal_in_reference.response_type)
                return

            # Set the data in goal_entry
            goal_entry.binary_value = binary_value
            goal_entry.save()

            # Understood
            understood_goal_response(current_user)


        elif(goal_in_reference.response_type == 2): # Text
            # Log response
            message_log.log_message('goal_prompt_response', current_user, text, None)

            # Set the data in goal_entry
            goal_entry.text_value = text
            goal_entry.save()

            # Send confirmation message and log
            understood_goal_response(current_user)

        else:
            misunderstood_goal_response(current_user, goal_in_reference.response_type)

def misunderstood_goal_response(current_user, correct_response_type):
    if correct_response_type == 0:
        misunderstood_goal_message = "I couldn't understand your response - make sure you reply with a number!"
    elif correct_response_type == 1:
        misunderstood_goal_message = "I couldn't understand your response - make sure you reply with yes or no!"

    # Send message
    send_api_helper.send_basic_text_message(current_user.fbid, misunderstood_goal_message)

    # Log message
    message_log.message_log('misunderstood_goal_message', current_user, misunderstood_goal_message, None)

def understood_goal_response(current_user):
    # Send confirmation message and log
    goal_response_received_confirmation = "Recorded! :)"
    send_api_helper.send_basic_text_message(current_user.fbid, goal_response_received_confirmation)
    message_log.message_log('goal_response_received_confirmation', current_user, goal_response_received_confirmation, None)