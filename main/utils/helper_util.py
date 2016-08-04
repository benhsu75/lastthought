from main.models import *

def user_exists(fbid):
    try:
        user = User.objects.get(fbid=fbid)
        return True
    except User.DoesNotExist:
        return False