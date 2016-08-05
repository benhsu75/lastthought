from main.models import *
from datetime import datetime

def user_exists(fbid):
    try:
        user = User.objects.get(fbid=fbid)
        return True
    except User.DoesNotExist:
        return False

def same_day(a, b):
    return (a - b).total_seconds() < 86400