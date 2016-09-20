from django.http import HttpResponse
from main.models import *
from main.entrypoints.messenger import send_api_helper

import random
from django.views.decorators.csrf import csrf_exempt
import json
from main.message_log import message_log
from main.utils import nlp, helper_util
from main.domains import (habits_domain,
                          logs_domain,
                          onboarding_domain,
                          misunderstood_domain)
import json
from django.shortcuts import redirect

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
            if not helper_util.user_exists(fbid):
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
                handle_optin(fbid)
            elif 'postback' in messaging:
                # Postback webhook
                payload = messaging['postback']['payload']
                handle_postback(fbid, payload)

    return HttpResponse(status=200)


@csrf_exempt
def account_link(request):
    account_linking_token = request.GET['account_linking_token']
    redirect_uri = request.GET['redirect_uri']

    # Get the PSID with the account_linking_token
    psid = get_psid_from_account_linking_token(account_linking_token)

    # Create the person's account
    print 'GOT PSID: ' + str(psid)

    return redirect('/')


def get_psid_from_account_linking_token(token):
    url_to_get = 'https://graph.facebook.com/v2.6/me?access_token={}&fields=recipient&account_linking_token={}'.format(constants.FB_PAGE_ACCESS_TOKEN, token)

    r = requests.get(url_to_get)

    print r.text

    psid = r.json()['recipient']

    return psid

# Sends the user our initial message
def handle_optin(fbid):
    # Check if user exists, if it does, do nothing
    try:
        current_user = User.objects.get(fbid=fbid)
        return  # Do nothing
    except User.DoesNotExist:
        pass

    onboarding_domain.create_new_user(fbid)

# When the user responds by tapping a quick reply
def handle_quick_reply(fbid, text, payload):
    state = payload['state']

    if helper_util.user_exists(fbid):
        current_user = User.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)
        # Should never get here

    # Switch on different quick reply states
    if state == 'habit_binary_response':
        habits_domain.handle_quick_reply(current_user, text, payload)
    elif state == 'log_context_response':
        logs_domain.apply_context_to_log(current_user, text, payload)
    else:
        misunderstood_domain.handle_misunderstood(current_user, text, text)

# Handles postbacks
def handle_postback(fbid, payload):
    try:
        current_user = User.objects.get(fbid=fbid)
    except User.DoesNotExist:
        send_api_helper.send_basic_text_message(
            fbid, "Something went wrong :("
        )
        return

    json_payload = json.loads(payload)
    print json_payload

    state = json_payload['state']

    if state == 'persistent_menu_view_logs':
        logs_domain.send_view_logs_message(current_user)
    else:
        # Error - never should reach here
        return

# When the user responds by sending any text message
def handle_message_received(fbid, text):
    try:
        current_user = User.objects.get(fbid=fbid)
    except User.DoesNotExist:
        send_api_helper.send_basic_text_message(
            fbid, "Something went wrong :("
        )
        return

    # Standardize text
    processed_text = text.strip().lower()

    # Use nlp to determine which domain it goes under,
    # then triage to that domain. The domain handles the
    # sub-triaging within itself

    if nlp.is_habits_domain(current_user, processed_text):
        habits_domain.handle_habits_text(current_user, text, processed_text)

    else:
        # Handle everything else as a log
        logs_domain.handle_logs_text(current_user, text, processed_text)

def handle_image_received(fbid, image_url):
    try:
        current_user = User.objects.get(fbid=fbid)
    except User.DoesNotExist:
        send_api_helper.send_basic_text_message(
            fbid, "Something went wrong :("
        )
        return

    logs_domain.handle_image_log_entry(current_user, image_url)