from main.models import *
from main.utils import constants, helper_util
from django.http import HttpResponse, HttpResponseRedirect
import requests
from main.api import foursquare, uber, instagram, fitbit

def foursquare_redirect(request, fbid):
    authorization_code = request.GET['code']

    user = User.objects.get(fbid=fbid)

    # Only OAuth if user hasn't connected foursquare yet
    try:
        foursquare_connection = FoursquareConnection.objects.get(user=user)
        return HttpResponseRedirect("/users/"+fbid+"/connect")
    except FoursquareConnection.DoesNotExist:
        pass

    redirect_uri = 'https://userdatagraph.herokuapp.com/foursquare_redirect'

    # Get access token
    token_url = 'https://foursquare.com/oauth2/access_token?client_id='+constants.FOURSQUARE_CLIENT_ID+'&client_secret='+constants.FOURSQUARE_CLIENT_SECRET+'&grant_type=authorization_code&redirect_uri='+redirect_uri+'&code=' + authorization_code
    r = requests.get(token_url)
    if 'access_token' in r.json():
        access_token = r.json()['access_token']

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
        return HttpResponseRedirect("/users/"+fbid+"/connect")
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

def instagram_redirect(request):
    authorization_code = request.GET['code']
    fbid = request.GET['state']

    user = User.objects.get(fbid=fbid)

    # Check if user has already OAuthed instagram
    try:
        # If user has already OAuthed, then no need to change data
        instagram_connection = InstagramConnection.objects.get(user=user)
        return HttpResponseRedirect("/users/"+fbid+"/connect")
        return
    except InstagramConnection.DoesNotExist:
        pass

    # Get refresh token
    payload = {
        'client_id' : constants.INSTAGRAM_CLIENT_ID,
        'client_secret' : constants.INSTAGRAM_CLIENT_SECRET,
        'grant_type' : 'authorization_code',
        'redirect_uri' : 'https://userdatagraph.herokuapp.com/instagram_redirect',
        'code' : authorization_code
    }
    token_url = 'https://api.instagram.com/oauth/access_token'

    print token_url

    r = requests.post(token_url, data=payload)

    print r.text

    if 'access_token' in r.json():
        access_token = r.json()['access_token']
        instagram_id = r.json()['user']['id']
        username = r.json()['user']['username']
        profile_picture = r.json()['user']['profile_picture']

    instagram_connection = InstagramConnection(is_connected_flag=True, access_token=access_token, user=user, instagram_id=instagram_id, username=username, profile_picture=profile_picture)
    instagram_connection.save()

    # Load all instagram data
    instagram.refresh_instagram_history(user)

    # Redirect
    return HttpResponseRedirect("/users/"+fbid+"/connect")

def fitbit_redirect(request):
    authorization_code = request.GET['code']
    fbid = request.GET['state']

    user = User.objects.get(fbid=fbid)

    # Check if user has already OAuthed fitbit
    try:
        # If user has already OAuthed, then no need to change data
        fitbit_connection = FitbitConnection.objects.get(user=user)
        return HttpResponseRedirect("/users/"+fbid+"/connect")
        return
    except FitbitConnection.DoesNotExist:
        pass

    # Get refresh token
    payload = {
        'client_id' : constants.FITBIT_CLIENT_ID,
        'client_secret' : constants.FITBIT_CLIENT_SECRET,
        'grant_type' : 'authorization_code',
        'redirect_uri' : 'https://userdatagraph.herokuapp.com/fitbit_redirect',
        'code' : authorization_code,
        'state' : fbid
    }

    token_url = 'https://api.fitbit.com/oauth2/token'

    r = requests.post(token_url, data=payload, auth=HTTPBasicAuth(constants.LYFT_CLIENT_ID, constants.LYFT_CLIENT_SECRET))

    print r.text

    if 'access_token' in r.json():
        access_token = r.json()['access_token']
        refresh_token = r.json()['refresh_token']
        fitbit_id = r.json()['user_id']

    # Create a fitbit connection
    fitbit_connection = FitbitConnection(is_connected_flag=True, refresh_token=refresh_token, user=user, fitbit_id=fitbit_id)
    fitbit_connection.save()

    # Get user's fitbit profile information
    profile_response = fitbit.get_profile_information(user, access_token)
    offsetFromUTCMillis = profile_response['user']['offsetFromUTCMillis']
    locale = profile_response['user']['locale']

    print 'Offset: ' + offsetFromUTCMillis
    print 'Locale: ' + locale

    # Refresh fitbit data
    fitbit.refresh_weight_history(user)

    # Redirect
    return HttpResponseRedirect("/users/"+fbid+"/connect")