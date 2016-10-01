from main.models import *
from datetime import datetime
from main.utils import helper_util


def is_logs_domain(current_profile, processed_text):
    if user_is_in_log_context_prompt_state(current_profile):
        return True
    return False


def is_view_domain(current_profile, processed_text):
    if processed_text == 'view':
        return True
    elif id_of_triggered_view_category(current_profile, processed_text) != -1:
        return True
    return False


##############################################
############### HELPER METHODS ###############
##############################################

def user_is_in_log_context_prompt_state(current_profile):
    messages_for_profile = Message.objects.filter(
        profile=current_profile
    )
    if len(messages_for_profile) == 0:
        return False

    last_message_type = messages_for_profile.order_by('-id')[0].message_type
    return last_message_type == 30


def id_of_triggered_view_category(current_profile, processed_text):
    user_log = Log.find_or_create(current_profile)

    categories = LogContext.objects.filter(log=user_log)

    # Check if it triggers each category
    for c in categories:
        category_name = c.context_name

        lowercase_category_name = category_name.strip().lower()

        if processed_text == lowercase_category_name:
            return c.id

    return -1
