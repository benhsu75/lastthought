import requests

FB_API_URL = 'https://graph.facebook.com/v2.7/'


# Hits the /me endpoint to get the user's id
def get_profile_info(access_token):
    user_profile_url = '{}me?access_token={}&fields=email'.format(
        FB_API_URL,
        access_token
    )

    r = requests.get(user_profile_url)

    real_fbid = None
    email = None

    if 'id' in r.json():
        real_fbid = r.json()['id']

    if 'email' in r.json():
        email = r.json()['email']

    return (real_fbid, email)
