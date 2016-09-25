from main.models import Message

# WE MUST FOLLOW THIS
# If it ends in 'message' it is sent TO the user
# If it ends in 'response' it is sent FROM the user

# EVERY message the user receives or sends should be logged.

# Mapping a message_key to the message_type that we store in the Message object
message_mapping = {
    'welcome_message': 0,
    'ask_for_name_message': 1,
    'name_response': 2,
    'nice_to_meet_message': 3,
    'learn_more_message': 4,
    'habit_prompt_message': 6,
    'habit_prompt_response': 7,
    'misunderstood_response': 9,
    'misunderstood_message': 10,
    'habits_trigger_message': 15,
    'habits_trigger_response': 16,
    'misunderstood_habit_response': 17,
    'misunderstood_habit_message': 18,
    'habit_creation_message': 19,
    'existing_habits_message': 20,
    'habit_info_message': 21,
    'help_response': 22,
    'log_new_entry_response': 27,
    'log_add_context_message': 28,
    'log_context_response': 29,
    'log_new_context_message': 30,
    'log_new_context_response': 31,
    'log_successful_context_message': 32,
    'log_trigger_listening_response' : 34,
    'log_listening_message' : 35,
    'log_invalid_trigger_message' : 36,
    'log_confirm_message' : 37,
    'log_view_message' : 38,
    'cancel_log_response' : 39,
    'cancel_log_message' : 40,
    'get_started_message' : 41,
    'categories_explanation_message' : 42,
    'sign_up_message' : 43,
    'finished_onboarding_message' : 44,
    'explain_link_message' : 45,
    'reminder_message' : 46
}


def log_message(message_key, profile, text, data):
    # Validate that message_key is valid
    if message_key not in message_mapping:
        return False

    # Determine if sent_to_user
    if 'message' in message_key:
        sent_to_user = True
    else:
        sent_to_user = False

    message_type = message_mapping[message_key]
    m = Message(
        profile=profile,
        sent_to_user=sent_to_user,
        message_type=message_type,
        text=text
    )
    m.save()

    # Add any extra data depending on message_type
    if message_type == 6:
        m.habit_entry_in_reference = data['habit_entry']
        m.save()
    elif message_type == 7:
        m.habit_entry_in_reference = data['habit_entry']
        m.save()

    return True
