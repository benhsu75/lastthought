from main.models import *
from datetime import datetime
from main.utils import helper_util

def is_logs_domain(current_profile, processed_text):
    if user_is_in_log_context_prompt_state(current_profile):
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
    return messages_for_profile.order_by('-id')[0].message_type == 30

