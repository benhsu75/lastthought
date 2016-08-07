from main.models import *
from datetime import datetime
from main.utils import helper_util


def is_onboarding_domain(current_user, text):
    return current_user.state == 0


def is_habits_domain(current_user, text):
    # Get the last message
    last_message = Message.objects.filter(
        user=current_user
    ).order_by('-created_at')[0]

    # Get the last prompt message
    prompt_message_list = Message.objects.filter(
        user=current_user,
        message_type=6
    ).order_by('-created_at')
    if len(prompt_message_list) > 0:
        last_prompt_message = prompt_message_list[0]
    else:
        last_prompt_message = None

    # NLP Stuff
    if('habits' in text):
        return True
    elif (
        last_message.message_type == 6 or
        last_prompt_message is not None and
        helper_util.same_day_as_now(last_prompt_message.created_at)
    ):
        return True
    else:
        return False


def is_logs_domain(text):
    return text.split()[0].lower() == "log:"


def is_todo_domain(current_user, text):
    return 'todo' in text
