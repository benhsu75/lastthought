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
from django.contrib.auth import login, authenticate, logout
from main.views import log_views


def fblogin_redirect(request):
    code = request.GET['code']

    # state won't be fbid if the user is logging in
    if 'state' in request.GET:
        login_flag = False
        fbid = request.GET['state']
    else:
        login_flag = True

    # Make request to get access_token
    if not login_flag:
        constructed_redirect_uri = constants.FB_LOGIN_REDIRECT_URI + "?state=" + fbid
    else:
        constructed_redirect_uri = constants.FB_LOGIN_REDIRECT_URI

    access_token_url = (
        "https://graph.facebook.com/v2.3/oauth/access_token?"
        "client_id={}&redirect_uri={}&client_secret={}&code={}"
    ).format(
        constants.FB_APP_ID,
        constructed_redirect_uri,
        constants.FB_CLIENT_SECRET,
        code)

    r = requests.get(access_token_url)

    access_token = r.json()['access_token']

    # Make request for user profile information e.g. fbid
    (real_fbid, email) = facebook.get_profile_info(access_token)

    # Check that getting profile info worked
    if not real_fbid:
        # Something wrong happened, error out
        x = 1

    if email:
        username = email
    else:
        username = real_fbid
    password = real_fbid

    try:
        profile = Profile.objects.get(global_fbid=real_fbid)

        # Log the user in
        user = profile.user

        user = authenticate(
            username=user.username,
            password=profile.global_fbid
        )

        if user is not None:
            login(request, user)
        else:
            # TODO
            x = 1
        return redirect('/')

    except Profile.DoesNotExist:
        if login_flag:
            # User is trying to login but doesn't have a profile,
            # so redirect them to the messenger bot to link the accounts

            # TODO
            return redirect('/try')
        else:
            # User is linking account
            profile = Profile.objects.get(fbid=fbid)

            # Create user
            user = User.objects.create_user(
                username=username,
                password=password
            )

            # Update profile
            profile.global_fbid = real_fbid
            profile.user = user

            # Set email if we got it
            if email:
                profile.email = email

            profile.save()

            # Log in user
            user = authenticate(username=user.username, password=real_fbid)
            if user is not None:
                'LOGGING USER IN'
                login(request, user)
            else:
                redirect('/')

            # Tell the user that they finished creating an account
            onboarding_domain.send_finished_onboarding_message(profile)

            # Get the user to share the LastThought bot
            onboarding_domain.send_share_message(profile)

            return redirect('/')


def fblogin_view(request, fbid, redirect_uri):
    # If logged in go to '/'
    if helper_util.authenticated_and_profile_exists(request):
        return redirect('/')

    # If user already linked account before
    profile = Profile.objects.get(fbid=fbid)
    if helper_util.user_has_created_account(profile):
        return redirect('/login')

    context = {
        'fbid': fbid,
        'redirect_uri': redirect_uri
    }
    template = loader.get_template('main/fblogin_view.html')
    return HttpResponse(template.render(context, request))


def logout_view(request):
    # Log the user out
    logout(request)

    # Redirect to home page
    return redirect('/')


def try_view(request):
    # If user logged in already
    if helper_util.authenticated_and_profile_exists(request):
        return redirect('/')

    # Return view
    context = {}
    template = loader.get_template('main/try.html')
    return HttpResponse(template.render(context, request))


def login_view(request):
    # If user logged in already
    if helper_util.authenticated_and_profile_exists(request):
        return redirect('/')

    # Return view
    context = {}
    template = loader.get_template('main/login.html')
    return HttpResponse(template.render(context, request))


def settings(request):
    # If user logged in already
    # if not helper_util.authenticated_and_profile_exists(request):
    #     return redirect('/login')

    # Return view
    context = {
        'user_id' : request.user.id
    }
    template = loader.get_template('main/settings.html')
    return HttpResponse(template.render(context, request))


def index(request):
    

    if helper_util.authenticated_and_profile_exists(request):
        # Get page number
        if 'page' in request.GET:
            page_no = request.GET['page']
        else:
            page_no = 1

        if hasattr(request.user, 'profile'):
            fbid = request.user.profile.fbid
            return log_views.index(request, fbid, page_no)

    context = {}
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context, request))

def search(request):
    if 'query' in request.GET:
        query_term = request.GET['query']
    else:
        return redirect('/')

    if helper_util.authenticated_and_profile_exists(request):
        if hasattr(request.user, 'profile'):
            fbid = request.user.profile.fbid
            return log_views.search(request, fbid, query_term)

    return redirect('/')

def terms(request):
    context = {}
    template = loader.get_template('main/terms.html')
    return HttpResponse(template.render(context, request))

def update_user(request, user_id):
    if request.method == 'POST':
        if 'reminder_settings' in request.POST:
            user = User.objects.get(id=user_id)

            profile = user.profile

            # Update setting
            profile.reminder_settings = request.POST['reminder_settings']
            profile.save()

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
    elif request.method == 'DELETE':

        user = User.objects.get(id=user_id)

        # Send message telling user that their account was deleted
        send_deleted_account_message(user.profile)

        # Delete user
        user.delete()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

def send_deleted_account_message(profile):
    deleted_account_message = "We've successfully deleted your account and all of your thoughts. We're sorry to see you leave :("
    send_api_helper.send_basic_text_message(profile.fbid, deleted_account_message)
    message_log.log_message('deleted_account_message', profile, deleted_account_message, None)

def connect(request, fbid):
    if not helper_util.profile_exists(fbid):
        return HttpResponse(status=404)
    profile = Profile.objects.get(fbid=fbid)

    context = {
        'lyft_connected_flag': user.rideshareinformation.lyft_connected_flag,
        'foursquare_connected_flag': hasattr(user, 'foursquareconnection') and profile.foursquareconnection.is_connected_flag,
        'lyft_connected_flag': hasattr(profile, 'lyftconnection') and profile.lyftconnection.is_connected_flag,
        'uber_connected_flag': hasattr(profile, 'uberconnection') and profile.uberconnection.is_connected_flag,
        'instagram_connected_flag': hasattr(profile, 'instagramconnection') and profile.instagramconnection.is_connected_flag,
        'fitbit_connected_flag': hasattr(profile, 'fitbitconnection') and profile.fitbitconnection.is_connected_flag,
        'gmail_connected_flag': False,  # hasattr(profile, 'gmailconnection') and profile.gmailconnection.is_connected_flag,
        'gcal_connected_flag': False,  # hasattr(profile, 'gcalconnection') and profile.gcalconnection.is_connected_flag,
        'gdrive_connected_flag': False,  # hasattr(profile, 'gdriveconnection') and profile.gdriveconnection.is_connected_flag,
        'facebook_connected_flag': False,  # hasattr(profile, 'facebookconnection') and profile.facebookconnection.is_connected_flag,
        'fbid': profile.fbid
    }

    template = loader.get_template('main/connect.html')
    return HttpResponse(template.render(context, request))
