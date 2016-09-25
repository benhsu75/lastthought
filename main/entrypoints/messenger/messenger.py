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
                          misunderstood_domain)
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
    print("------RECEIVED MESSAGE (BODY BELOW)------")
    print(body)
    print("------DONE PRINTING------------")

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
                        # TODO
                        x = 1
                    elif attachment_type == 'audio':
                        # TODO
                        x = 1
                    elif attachment_type == 'location':
                        # TODO 
                        x = 1
                    else:
                        print 'COULD NOT HANDLE THIS ATTACHMENT TYPE: ' + attachment_type
                    continue
                # Is normal message received
                elif 'text' in messaging['message']:
                    message_text = messaging['message']['text']
                    handle_message_received(fbid, message_text)
                    continue
                else:
                    print 'COULD NOT HANDLE'
                    # TODO
            elif 'optin' in messaging:
                # Plugin authentication webhook
                handle_optin(messaging)
            elif 'postback' in messaging:
                # Postback webhook
                payload = messaging['postback']['payload']
                handle_postback(fbid, payload)

    return HttpResponse(status=200)


@csrf_exempt
def account_link(request):
    print 'in account_link'
    account_linking_token = request.GET['account_linking_token']
    redirect_uri = request.GET['redirect_uri']

    # Get the PSID with the account_linking_token
    psid = get_psid_from_account_linking_token(account_linking_token)

    print 'PSID: ' + psid

    return general.fblogin_view(request, psid, redirect_uri)

def get_psid_from_account_linking_token(token):
    print 'get_psid_from_account_linking_token'
    url_to_get = 'https://graph.facebook.com/v2.6/me?access_token={}&fields=recipient&account_linking_token={}'.format(constants.FB_PAGE_ACCESS_TOKEN, token)

    r = requests.get(url_to_get)

    print r.text

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
    else:
        misunderstood_domain.handle_misunderstood(current_profile, text, text)

# Handles postbacks
def handle_postback(fbid, payload):
    try:
        current_profile = Profile.objects.get(fbid=fbid)
    except Profile.DoesNotExist:
        onboarding_domain.create_new_user(fbid)

    json_payload = json.loads(payload)
    print 'HANDLE POSTBACK'
    print json_payload

    state = json_payload['state']

    if state == 'persistent_menu_view_logs':
        if helper_util.user_has_created_account(current_profile): 
            logs_domain.send_view_logs_message(current_profile)
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
    
    # Handle everything else as a log
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