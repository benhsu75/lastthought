from main.models import *
from datetime import datetime
from django.utils import timezone

def user_exists(fbid):
    try:
        user = User.objects.get(fbid=fbid)
        return True
    except User.DoesNotExist:
        return False

def same_day_as_now(a):
    return (datetime.now(timezone.utc) - a).total_seconds() < 86400