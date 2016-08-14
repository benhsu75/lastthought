from main.models import *
from datetime import datetime
from main.utils import helper_util


def is_help_domain(processed_text):
    return processed_text == 'help'


def is_habits_domain(current_user, processed_text):
    # NLP Stuff
    if('habits' in processed_text):
        return True
    elif user_is_in_habit_answer_prompt_state(current_user):
        return True
    else:
        return False


def is_logs_domain(current_user, processed_text):
    if processed_text.startswith('log'):
        return True
    elif user_is_in_log_entry_state(current_user):
        return True
    elif user_is_in_log_context_prompt_state(current_user):
        return True
    return False


def is_todo_domain(current_user, processed_text):
    if 'todo' in processed_text:
        return True
    elif user_is_in_complete_todo_state(processed_text, current_user):
        return True
    else:
        return False


def is_weather_domain(processed_text):
    if 'weather' in processed_text:
        return True


def is_ridesharing_domain(processed_text):
    if 'ride' in processed_text:
        return True

##############################################
############### HELPER METHODS ###############
##############################################


# Returns whether or not the last message in the message log
# was us prompting a response
def last_message_is_habit_prompt(current_user):
    return Message.objects.filter(
        user=current_user
    ).order_by('-id')[0].message_type == 6


def last_message_is_show_todo(current_user):
    return Message.objects.filter(
        user=current_user
    ).order_by('-id')[0].message_type == 11


def last_message_is_incorrect_index_message(current_user):
    return Message.objects.filter(
        user=current_user
    ).order_by('-id')[0].message_type == 24

def last_message_is_listening_message(current_user):
    return Message.objects.filter(
        user=current_user
    ).order_by('-id')[0].message_type == 35

# Looks at the message history, and returns whether or not this
# message is a response to a prompt
def user_is_in_habit_answer_prompt_state(current_user):
    if last_message_is_habit_prompt(current_user):
        return True

    # Get last prompt message
    prompt_message_list = Message.objects.filter(
        user=current_user,
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


def user_is_in_log_context_prompt_state(current_user):
    return Message.objects.filter(
        user=current_user
    ).order_by('-id')[0].message_type == 30



def user_is_in_complete_todo_state(processed_text, current_user):
    try:
        int(processed_text)
    except ValueError:
        return False

    if last_message_is_show_todo(current_user):
        return True

    if last_message_is_incorrect_index_message(current_user):
        return True

    return False

def user_is_in_log_entry_state(current_user):
    if last_message_is_listening_message(current_user):
        return True
    else:
        return False
