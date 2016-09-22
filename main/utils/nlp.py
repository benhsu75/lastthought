from main.models import *
from datetime import datetime
from main.utils import helper_util


def is_habits_domain(current_profile, processed_text):
    # NLP Stuff
    if('habits' in processed_text):
        return True
    elif user_is_in_habit_answer_prompt_state(current_profile):
        return True
    else:
        return False


def is_logs_domain(current_profile, processed_text):
    if user_is_in_log_context_prompt_state(current_profile):
        return True
    return False


##############################################
############### HELPER METHODS ###############
##############################################


# Returns whether or not the last message in the message log
# was us prompting a response
def last_message_is_habit_prompt(current_profile):
    return Message.objects.filter(
        profile=current_profile
    ).order_by('-id')[0].message_type == 6

# Looks at the message history, and returns whether or not this
# message is a response to a prompt
def user_is_in_habit_answer_prompt_state(current_profile):
    if last_message_is_habit_prompt(current_profile):
        return True

    # Get last prompt message
    prompt_message_list = Message.objects.filter(
        profile=current_profile,
        message_type=6
    ).order_by('-id')
    if len(prompt_message_list) > 0:
        last_prompt_message = prompt_message_list[0]
    else:
        return False

    # Check if prompt has bee answered
    if last_prompt_message.habit_entry_in_reference.response_collected:
        return False

    # Get all messages newer than the last_prompt_message
    newer_messages = Message.objects.filter(id__gte=last_prompt_message.id)

    accepted_message_types = [6, 17, 18]

    for m in newer_messages:
        print 'message type is this message is ' + str(m.message_type)
        if m.message_type not in accepted_message_types:
            return False

    return True


def user_is_in_log_context_prompt_state(current_profile):
    return Message.objects.filter(
        profile=current_profile
    ).order_by('-id')[0].message_type == 30

