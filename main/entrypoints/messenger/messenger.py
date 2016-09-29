from django.http import HttpResponse
from main.models import *
from main.entrypoints.messenger import send_api_helper

import random
from django.views.decorators.csrf import csrf_exempt
import json
from main.message_log import message_log
from main.utils import nlp, helper_util
from main.domains import (logs_domain,
                          onboarding_domain,
                          misunderstood_domain,
                          view_logs_domain)
import json
from django.shortcuts import redirect
from main.utils import constants
import requests
from main.views import general

######################################
######### MESSENGER WEBHOOK ##########
######################################

@csrf_exempt
def messenger_callback(request):
    if('hub.challenge' in request.GET):
        return HttpResponse(request.GET['hub.challenge'])

    # Get body from request
    body = json.loads(request.body)

    # Print request for debugging
    print "------RECEIVED MESSAGE (BODY BELOW)------" 
    print body 
    print '\n'

    # Loop through multiple entries
    entry_list = body['entry']
    for entry in entry_list:
        page_id = entry['id']
        timestamp = entry['time']
        messaging_list = entry['messaging']

        for messaging in messaging_list:

            fbid = messaging['sender']['id']

            # If user doesn't exist, then start onboarding flow and create new user
            if not helper_util.profile_exists(fbid):
                onboarding_domain.create_new_user(fbid)
                continue

            # Handle different webhooks times
            if 'message' in messaging:
                # Reroute quick replies
                if 'quick_reply' in messaging['message']:
                    message_text = messaging['message']['text']
                    payload = json.loads(
                        messaging['message']['quick_reply']['payload']
                    )

                    handle_quick_reply(fbid, message_text, payload)
                    continue

                # Reroute messages with attachments
                elif 'attachments' in messaging['message']:
                    attachment_type = messaging['message']['attachments'][0]['type']

                    # Images
                    if attachment_type == 'image':
                        for image in messaging['message']['attachments']:
                            image_url = image['payload']['url']

                            handle_image_received(fbid, image_url)
                            continue
                    # Video
                    elif attachment_type == 'video':
                        send_cant_handle_message_type_message(fbid, "video")
                    elif attachment_type == 'audio':
                        send_cant_handle_message_type_message(fbid, "audio")
                    elif attachment_type == 'location':
                        send_cant_handle_message_type_message(fbid, "locations")
                    else:
                        send_cant_handle_message_type_message(fbid, "this content type")
                    continue
                # Is normal message received
                elif 'text' in messaging['message']:
                    message_text = messaging['message']['text']
                    handle_message_received(fbid, message_text)
                    continue
                else:
                    send_cant_handle_message_type_message(fbid, "this content type")
            elif 'optin' in messaging:
                # Plugin authentication webhook
                handle_optin(messaging)
            elif 'postback' in messaging:
                # Postback webhook
                payload = messaging['postback']['payload']
                handle_postback(fbid, payload)

    return HttpResponse(status=200)

def send_cant_handle_message_type_message(fbid, message_type):
    cant_handle_message_type_message = "Unfortunately, we can't yet handle {} :(. Please send me text or an image and keep that for you!".format(message_type)
    send_api_helper.send_basic_text_message(fbid, cant_handle_message_type_message)
    try:
        current_profile = Profile.objects.get(id=fbid)
        message_log.log_message('cant_handle_message_type_message', current_profile, get_started_message, None)
    except Profile.DoesNotExist:
        return

@csrf_exempt
def account_link(request):
    account_linking_token = request.GET['account_linking_token']
    redirect_uri = request.GET['redirect_uri']

    # Get the PSID with the account_linking_token
    psid = get_psid_from_account_linking_token(account_linking_token)

    return general.fblogin_view(request, psid, redirect_uri)

def get_psid_from_account_linking_token(token):
    url_to_get = 'https://graph.facebook.com/v2.6/me?access_token={}&fields=recipient&account_linking_token={}'.format(constants.FB_PAGE_ACCESS_TOKEN, token)

    r = requests.get(url_to_get)

    psid = r.json()['recipient']

    return psid

# Sends the user our initial message
def handle_optin(messaging):
    # Get pass through param
    pass_through_param = messaging['optin']['ref']
    fbid = messaging['sender']['id']

    if pass_through_param == 'TRY':
        # Check if profile exists
        if helper_util.profile_exists(fbid):
            profile = Profile.objects.get(fbid=fbid)
            onboarding_domain.send_almost_done_message(profile)
            onboarding_domain.send_create_account_message(profile)
        else:
            onboarding_domain.create_new_user(fbid)

# When the user responds by tapping a quick reply
def handle_quick_reply(fbid, text, payload):
    state = payload['state']

    if helper_util.profile_exists(fbid):
        current_profile = Profile.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)
        # Should never get here

    # Switch on different quick reply states
    if state == 'log_context_response':
        logs_domain.apply_context_to_log(current_profile, text, payload)
    elif state == 'cancel_new_category':
        logs_domain.send_successful_new_category_cancel(current_profile)
    else:
        misunderstood_domain.handle_misunderstood(current_profile, text, text)

# Handles postbacks
def handle_postback(fbid, payload):
    try:
        current_profile = Profile.objects.get(fbid=fbid)
    except Profile.DoesNotExist:
        onboarding_domain.create_new_user(fbid)

    json_payload = json.loads(payload)

    state = json_payload['state']

    if state == 'persistent_menu_view_logs':
        if helper_util.user_has_created_account(current_profile): 
            view_logs_domain.send_view_logs_message(current_profile)
        else:
            # Tell user to link account before viewing logs
            explain_link_message = 'Before you can view your logs, create an account here:'
            send_api_helper.send_basic_text_message(current_profile.fbid, explain_link_message)
            message_log.log_message('explain_link_message', current_profile, explain_link_message, None)

            onboarding_domain.send_create_account_message(current_profile)
    elif state == 'get_started':
        # Create user
        onboarding_domain.create_new_user(fbid)
    else:
        # Error - never should reach here
        return

# When the user responds by sending any text message
def handle_message_received(fbid, text):
    try:
        current_profile = Profile.objects.get(fbid=fbid)
    except Profile.DoesNotExist:
        send_api_helper.send_basic_text_message(
            fbid, "Something went wrong :("
        )
        return

    # Standardize text
    processed_text = text.strip().lower()
    
    # Use NLP to route
    if nlp.is_view_domain(current_profile, processed_text):
        view_logs_domain.send_view_logs_message(current_profile)
    else:
        logs_domain.handle_logs_text(current_profile, text, processed_text)

def handle_image_received(fbid, image_url):
    try:
        current_profile = Profile.objects.get(fbid=fbid)
    except Profile.DoesNotExist:
        send_api_helper.send_basic_text_message(
            fbid, "Something went wrong :("
        )
        return

    logs_domain.handle_image_log_entry(current_profile, image_url)