from main.models import Message

# WE MUST FOLLOW THIS
# If it ends in 'message' it is sent TO the user
# If it ends in 'response' it is sent FROM the user

# EVERY message the user receives or sends should be logged.

# Mapping a message_key to the message_type that we store in the Message object
message_mapping = {
    'welcome_message': 0,
    'learn_more_message': 4,
    'habit_prompt_message': 6,
    'habit_prompt_response': 7,
    'misunderstood_response': 9,
    'misunderstood_message': 10,
    'log_new_entry_response': 27,
    'log_add_context_message': 28,
    'log_context_response': 29,
    'log_new_context_message': 30,
    'log_new_context_response': 31,
    'log_successful_context_message': 32,
    'log_confirm_message' : 37,
    'log_view_message' : 38,
    'get_started_message' : 41,
    'categories_explanation_message' : 42,
    'sign_up_message' : 43,
    'finished_onboarding_message' : 44,
    'explain_link_message' : 45,
    'reminder_message' : 46,
    'max_number_categories_message' : 47,
    'cant_handle_message_type_message' : 48,
    'weekly_message' : 49,
    'send_successful_new_category_cancel' : 50,
    'share_message' : 51
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
