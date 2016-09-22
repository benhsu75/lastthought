from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import helper_util, nlp, constants

def handle_habits_text(current_profile, text, processed_text):

    # Get context
    fbid = current_profile.fbid

    # Send message
    if 'habits' in processed_text:
        # Log response
        message_log.log_message('habits_trigger_response', current_profile, text, None)

        # Send list of habits and links to view them
        habit_list = Habit.objects.filter(profile=current_profile)

        if len(habit_list) == 0:
            # Tell user that we are sending them their existing habits
            existing_habits_message = "You have no habits yet."
            
        else:
            # Tell user that we are sending them their existing habits
            existing_habits_message = "Here are your existing habits:"
            
        # Send message
        send_api_helper.send_basic_text_message(fbid, existing_habits_message)
        # Log message
        message_log.log_message('existing_habits_message', current_profile, existing_habits_message, None)

        for habit in habit_list:
            # Send list of habits
            habit_info_message = "" + habit.name + " - " + habit.send_text
            # Send message
            send_api_helper.send_button_message(fbid, habit_info_message, [
                    {
                        'type': 'web_url',
                        'url': constants.BASE_HEROKU_URL + '/habits/'+str(habit.id)+'/show',
                        'title': 'View'    
                    },
                ])
            # Log message
            message_log.log_message('habit_info_message', current_profile, habit_info_message, None)

        # Send manage message
        habits_trigger_message = "Manage your habits:"
        send_api_helper.send_button_message(fbid, habits_trigger_message, [
                    {
                        'type': 'web_url',
                        'url': constants.BASE_HEROKU_URL + '/users/'+fbid+'/habits',
                        'title': 'See Habits'    
                    },
                    {
                        'type': 'web_url',
                        'url': constants.BASE_HEROKU_URL + '/users/'+fbid+'/add_habit',
                        'title': 'Add Habit'    
                    }
                ])
        message_log.log_message('habits_trigger_message', current_profile, habits_trigger_message, None)
    elif nlp.user_is_in_habit_answer_prompt_state(current_profile):

        # Get last prompt message
        prompt_message_list = Message.objects.filter(
            profile=current_profile,
            message_type=6
        ).order_by('-created_at')
        last_prompt_message = prompt_message_list[0]

        # Triage and store
        habit_entry = last_prompt_message.habit_entry_in_reference

        if(habit_entry.habit.response_type == 0): # Numeric
            # Convert to float
            try:
                val = float(processed_text)
            except:
                # Log response
                message_log.log_message('misunderstood_habit_response', current_profile, text, None)
                misunderstood_habit_response(current_profile, habit_entry.habit.response_type)
                return

            # Log response
            message_log.log_message('habit_prompt_response', current_profile, text, {'habit_entry':habit_entry})
            
            # Set the data in habit_entry
            habit_entry.numeric_value = val
            habit_entry.save()

            # Understood!
            understood_habit_response(current_profile, last_prompt_message)

        elif(habit_entry.habit.response_type  == 1): # Binary
            # Convert text to 0 or 1
            if processed_text in constants.AFFIRMATIVE_SYNONYMS:
                binary_value = 1
            elif processed_text in constants.NEGATIVE_SYNONYMS:
                binary_value = 0
            else:
                # Log invalid response
                message_log.log_message('misunderstood_habit_response', current_profile, text, None)

                # Send message
                misunderstood_habit_response(current_profile, habit_entry.habit.response_type)
                return

            # Log response
            message_log.log_message('habit_prompt_response', current_profile, text, {'habit_entry':habit_entry})

            # Set the data in habit_entry
            habit_entry.binary_value = binary_value
            habit_entry.save()

            # Understood
            understood_habit_response(current_profile, last_prompt_message)


        elif(habit_entry.habit.response_type == 2): # Text
            # Log response
            message_log.log_message('habit_prompt_response', current_profile, text, {'habit_entry':habit_entry})

            # Set the data in habit_entry
            habit_entry.text_value = text
            habit_entry.save()

            # Send confirmation message and log
            understood_habit_response(current_profile, last_prompt_message)

        else:
            misunderstood_habit_response(current_profile, habit_entry.habit.response_type)

def handle_quick_reply(current_profile, text, payload):

    # Get data from payload
    habit_entry_id = payload['habit_entry_id']
    habit_entry = HabitEntry.objects.get(id=habit_entry_id)

    # Record habit entry
    habit_entry.binary_value = payload['value']
    habit_entry.response_collected = 1
    habit_entry.save()

    # Log message
    message_log.log_message('habit_prompt_response', current_profile, text, {'habit_entry':habit_entry})

    # Send confirmation message and log
    send_recorded_message(current_profile)

def misunderstood_habit_response(current_profile, correct_response_type):
    if correct_response_type == 0:
        misunderstood_habit_message = "I couldn't understand your response - make sure you reply with a number!"
    elif correct_response_type == 1:
        misunderstood_habit_message = "I couldn't understand your response - make sure you reply with yes or no!"

    # Send message
    send_api_helper.send_basic_text_message(current_profile.fbid, misunderstood_habit_message)

    # Log message
    message_log.log_message('misunderstood_habit_message', current_profile, misunderstood_habit_message, None)

def understood_habit_response(current_profile, original_message):
    send_recorded_message(current_profile)
    
    # Mark the original message as resolved
    original_message.habit_entry_in_reference.response_collected = 1
    original_message.habit_entry_in_reference.save()

def send_recorded_message(current_profile):
    # Send confirmation message and log
    habit_response_received_confirmation = "Recorded! :)"
    send_api_helper.send_basic_text_message(current_profile.fbid, habit_response_received_confirmation)
    message_log.log_message('habit_response_received_confirmation', current_profile, habit_response_received_confirmation, None)
