from main.models import *
from main.utils import constants, helper_util
from django.http import HttpResponse, HttpResponseRedirect

def foursquare_redirect(request, fbid):
    authorization_code = request.GET['code']

    redirect_uri = 'https://userdatagraph.herokuapp.com/foursquare_redirect'

    # Get access token
    token_url = 'https://foursquare.com/oauth2/access_token?client_id='+constants.FOURSQUARE_CLIENT_ID+'&client_secret='+constants.FOURSQURE_CLIENT_SECRET+'&grant_type=authorization_code&redirect_uri='+redirect_uri+'&code=' + authorization_code
    r = requests.get(token_url)
    if 'access_token' in r.json():
        access_token = r.json()['access_token']

    print 'GOT FOURSQUARE ACCESS TOKEN'
    print access_token

    print fbid

    user = User.objects.get(fbid=fbid)
    user.foursquare_connected_flag = True
    user.foursquare_access_token = access_token
    user.save()

    # Load all the foursquare data

    # Redirect to ridesharing_setup page
    return HttpResponseRedirect("/users/"+fbid+"/connect")