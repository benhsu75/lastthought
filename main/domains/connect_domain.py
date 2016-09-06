from main.models import *
from main.utils import constants, helper_util
from django.http import HttpResponse, HttpResponseRedirect
import requests
from main.api import foursquare, uber

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

def uber_redirect(request):

    authorization_code = request.GET['code']
    fbid = request.GET['state']

    print authorization_code
    print fbid

    user = User.objects.get(fbid=fbid)

    # Check if user has already OAuthed uber
    try:
        # If user has already OAuthed, then no need to change data
        uber_connection = UberConnection.objects.get(user=user)
        return
    except UberConnection.DoesNotExist:
        pass

    # Get refresh token
    payload = {
        'client_id' : constants.UBER_CLIENT_ID,
        'client_secret' : constants.UBER_CLIENT_SECRET,
        'grant_type' : 'authorization_code',
        'redirect_uri' : 'https://userdatagraph.herokuapp.com/uber_redirect/',
        'code' : authorization_code
    }
    token_url = 'https://login.uber.com/oauth/v2/token'

    print token_url

    r = requests.post(token_url, data=payload)

    print r.text

    if 'refresh_token' in r.json():
        refresh_token = r.json()['refresh_token']

    uber_connection = UberConnection(is_connected_flag=True, refresh_token=refresh_token, user=user)
    uber_connection.save()

    # Load all uber data
    uber.refresh_ride_history(user)

    # Redirect
    return HttpResponseRedirect("/users/"+fbid+"/connect")
