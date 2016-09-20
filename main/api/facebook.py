import requests

FB_API_URL = 'https://graph.api.com/v2.7/'

def get_fb_profile_info(access_token):
    user_profile_url = '{}me?access_token={}'.format(FB_API_URL, access_token)

    r = requests.get(user_profile_url)

    print r.text

    