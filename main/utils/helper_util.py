from main.models import *
from datetime import datetime
from django.utils import timezone

def profile_exists(fbid):
    try:
        profile = Profile.objects.get(fbid=fbid)
        return True
    except Profile.DoesNotExist:
        return False

def user_has_created_account(profile):
    return hasattr(profile, 'user')

def same_day_as_now(a):
    return (datetime.now(timezone.utc) - a).total_seconds() < 86400

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
