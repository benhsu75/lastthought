import requests
from main.utils import constants
import json

def get_user_profile_data(fbid):
    url_to_get = constants.GRAPH_BASE_URL + str(fbid) + '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=' + constants.FB_PAGE_ACCESS_TOKEN
    print url_to_get
    r = requests.get(url_to_get)
    response = json.loads(r.text)
    print r.text
    return (
            response['first_name'],
            response['last_name'],
            response['profile_pic'],
            response['locale'],
            response['timezone'],
            response['gender'],
        )

