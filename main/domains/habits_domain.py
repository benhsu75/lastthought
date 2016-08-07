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

def handle_habits_text(current_user, text):

    print 'handle_habits_text in habits_domain'

    # Get context
    fbid = current_user.fbid
    
    last_message = Message.objects.filter(user=current_user).order_by('-created_at')[0]
    prompt_message_list = Message.objects.filter(user=current_user, message_type=6).order_by('-created_at')
    
    if len(prompt_message_list) > 0:
        last_prompt_message = prompt_message_list[0]
    else:
        last_prompt_message = None
    
    # Send message
    if 'habits' in text:
        # Log response
        message_log.log_message('habits_trigger_response', current_user, text, None)

        # Send message
        habits_trigger_message = "Manage your habits:"
        send_api_helper.send_button_message(fbid, habits_trigger_message, [
                    {
                        'type': 'web_url',
                        'url': BASE_HEROKU_URL + '/users/'+fbid+'/habits',
                        'title': 'See Habits'    
                    },
                    {
                        'type': 'web_url',
                        'url': BASE_HEROKU_URL + '/users/'+fbid+'/add_habit',
                        'title': 'Add Habit'    
                    }
                ])
        message_log.log_message('habits_trigger_message', current_user, habits_trigger_message, None)
    elif(last_message.message_type  == 6 or (last_prompt_message != None and helper_util.same_day_as_now(last_prompt_message.created_at))):
        print 'going to triage'
        # Triage and store
        habit_in_reference = last_prompt_message.habit_in_reference
        habit_entry = HabitEntry.objects.filter(habit=habit_in_reference).order_by('-created_at')[0]

        if(habit_in_reference.response_type == 0): # Numeric
            # Convert to float
            try:
                val = float(text)
            except:
                # Log response
                message_log.log_message('misunderstood_habit_response', current_user, text, None)
                misunderstood_habit_response(current_user, habit_in_reference.response_type)
                return

            # Log response
            message_log.log_message('habit_prompt_response', current_user, text, {'habit':habit_in_reference})
            
            # Set the data in habit_entry
            habit_entry.numeric_value = val
            habit_entry.save()

            # Understood!
            understood_habit_response(current_user, last_prompt_message)

        elif(habit_in_reference.response_type == 1): # Binary
            # Convert text to 0 or 1
            processed_text = text.strip().lower()
            if processed_text in affirmative_synonyms:
                binary_value = 1
            elif processed_text in negative_synonyms:
                binary_value = 0
            else:
                # Log invalid response
                message_log.log_message('misunderstood_habit_response', current_user, text, None)

                # Send message
                misunderstood_habit_response(current_user, habit_in_reference.response_type)
                return

            # Log response
            message_log.log_message('habit_prompt_response', current_user, text, {'habit':habit_in_reference})

            # Set the data in habit_entry
            habit_entry.binary_value = binary_value
            habit_entry.save()

            # Understood
            understood_habit_response(current_user, last_prompt_message)


        elif(habit_in_reference.response_type == 2): # Text
            # Log response
            message_log.log_message('habit_prompt_response', current_user, text, {'habit':habit_in_reference})

            # Set the data in habit_entry
            habit_entry.text_value = text
            habit_entry.save()

            # Send confirmation message and log
            understood_habit_response(current_user, last_prompt_message)

        else:
            misunderstood_habit_response(current_user, habit_in_reference.response_type)

def handle_quick_reply(current_user, text, payload):

    # Get data from payload
    habit_entry_id = payload['habit_entry_id']
    habit_entry = HabitEntry.objects.get(id=habit_entry_id)

    # Record habit entry
    habit_entry.binary_value = payload['value']
    habit_entry.response_collected = 1
    habit_entry.save()

    # Log message
    message_log.log_message('habit_prompt_response', current_user, text, {'habit':habit_entry.habit})

    # Send confirmation message and log
    send_recorded_message(current_user)

def misunderstood_habit_response(current_user, correct_response_type):
    if correct_response_type == 0:
        misunderstood_habit_message = "I couldn't understand your response - make sure you reply with a number!"
    elif correct_response_type == 1:
        misunderstood_habit_message = "I couldn't understand your response - make sure you reply with yes or no!"

    # Send message
    send_api_helper.send_basic_text_message(current_user.fbid, misunderstood_habit_message)

    # Log message
    message_log.log_message('misunderstood_habit_message', current_user, misunderstood_habit_message, None)

def understood_habit_response(current_user, original_message):
    send_recorded_message(current_user)
    
    # Mark the original message as resolved
    original_message.response_captured = True
    original_message.save()

def send_recorded_message(current_user):
    # Send confirmation message and log
    habit_response_received_confirmation = "Recorded! :)"
    send_api_helper.send_basic_text_message(current_user.fbid, habit_response_received_confirmation)
    message_log.log_message('habit_response_received_confirmation', current_user, habit_response_received_confirmation, None)
