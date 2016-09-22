import requests

FB_API_URL = 'https://graph.facebook.com/v2.7/'

# Hits the /me endpoint to get the user's id
def get_fb_profile_info(access_token):
    user_profile_url = '{}me?access_token={}'.format(FB_API_URL, access_token)

    print 'Going to GET: ' + user_profile_url

    r = requests.get(user_profile_url)

    print r.text

    real_fbid = r.json()['id']

    return real_fbid

    