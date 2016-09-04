from main.models import *
from main.utils import constants, helper_util
from django.http import HttpResponse, HttpResponseRedirect
import requests
from main.api import foursquare

def foursquare_redirect(request, fbid):
    authorization_code = request.GET['code']

    redirect_uri = 'https://userdatagraph.herokuapp.com/foursquare_redirect'

    # Get access token
    token_url = 'https://foursquare.com/oauth2/access_token?client_id='+constants.FOURSQUARE_CLIENT_ID+'&client_secret='+constants.FOURSQUARE_CLIENT_SECRET+'&grant_type=authorization_code&redirect_uri='+redirect_uri+'&code=' + authorization_code
    r = requests.get(token_url)
    if 'access_token' in r.json():
        access_token = r.json()['access_token']

    user = User.objects.get(fbid=fbid)

    try:
        foursquare_connection = FoursquareConnection.objects.get(user=user)
    except FoursquareConnection.DoesNotExist:
        foursquare_connection = FoursquareConnection(is_connected_flag=True, access_token=access_token, user=user)
        foursquare_connection.save()

    # Load all the foursquare data
    foursquare.refresh_checkin_history(user)

    # Redirect to ridesharing_setup page
    return HttpResponseRedirect("/users/"+fbid+"/connect")