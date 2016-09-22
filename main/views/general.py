from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *
from main.utils import helper_util, constants
import requests
from django.shortcuts import redirect
from main.api import facebook
from main.domains import onboarding_domain
from django.contrib.auth.models import User

def fblogin_redirect(request):
    code = request.GET['code']
    fbid = request.GET['state']

    print 'IN FB LOGIN REDIRECT'
    print 'STATE ' + fbid

    # Make request to get access_token
    constructed_redirect_uri = constants.FB_LOGIN_REDIRECT_URI + "?state=" + fbid
    access_token_url = 'https://graph.facebook.com/v2.3/oauth/access_token?client_id={}&redirect_uri={}&client_secret={}&code={}'.format(constants.FB_APP_ID, constructed_redirect_uri, constants.FB_CLIENT_SECRET, code)

    r = requests.get(access_token_url)

    print r.text

    access_token = r.json()['access_token']

    # Make request for user profile information e.g. fbid
    real_fbid = facebook.get_fb_profile_info(access_token)

    # Create full account
    profile = Profile.objects.get(fbid=fbid)

    # Check if profile already has user account
    if helper_util.user_has_created_account(profile):
        # Don't do anything
        x = 1
    else:
        # Update profile
        profile.global_fbid = real_fbid
        profile.save()

        # Create user
        # user = User(username=, password=real_fbid)

    # Tell the user that they finished creating an account
    onboarding_domain.send_finished_onboarding_message(profile)

    return redirect('/')

def fblogin_view(request, fbid, redirect_uri):
    context = RequestContext(request, {
        'fbid' : fbid,
        'redirect_uri' : redirect_uri
        })
    template = loader.get_template('main/fblogin_view.html')
    return HttpResponse(template.render(context))

def index(request):    
    context = RequestContext(request, {})
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context))

def learn_more(request):
    context = RequestContext(request, {})
    template = loader.get_template('main/learn_more.html')
    return HttpResponse(template.render(context))

def connect(request, fbid):
    if not helper_util.profile_exists(fbid):
        return HttpResponse(status=404)
    profile = Profile.objects.get(fbid=fbid)

    context = RequestContext(request, {
        'lyft_connected_flag' : user.rideshareinformation.lyft_connected_flag,
        'foursquare_connected_flag' : hasattr(user,'foursquareconnection') and profile.foursquareconnection.is_connected_flag,
        'lyft_connected_flag' : hasattr(profile,'lyftconnection') and profile.lyftconnection.is_connected_flag,
        'uber_connected_flag' : hasattr(profile, 'uberconnection') and profile.uberconnection.is_connected_flag,
        'instagram_connected_flag' : hasattr(profile, 'instagramconnection') and profile.instagramconnection.is_connected_flag,
        'fitbit_connected_flag' : hasattr(profile, 'fitbitconnection') and profile.fitbitconnection.is_connected_flag,
        'gmail_connected_flag' : False,#hasattr(profile, 'gmailconnection') and profile.gmailconnection.is_connected_flag,
        'gcal_connected_flag' : False,#hasattr(profile, 'gcalconnection') and profile.gcalconnection.is_connected_flag,
        'gdrive_connected_flag' : False,#hasattr(profile, 'gdriveconnection') and profile.gdriveconnection.is_connected_flag,
        'facebook_connected_flag' : False,#hasattr(profile, 'facebookconnection') and profile.facebookconnection.is_connected_flag,
        'fbid' : profile.fbid
        
        })
    template = loader.get_template('main/connect.html')
    return HttpResponse(template.render(context))
