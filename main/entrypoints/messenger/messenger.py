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
                          todo_domain,
                          misunderstood_domain,
                          help_domain,
                          ridesharing_domain)

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

            # Create new user
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

                # Is normal message received
                message_text = messaging['message']['text']
                handle_message_received(fbid, message_text)
            elif 'optin' in messaging:
                # Plugin authentication webhook
                handle_optin(fbid)
            elif 'postback' in messaging:
                # Postback webhook
                payload = messaging['postback']['payload']
                handle_postback(fbid, payload)

    return HttpResponse(status=200)


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
    if state == 'log_context_response':
        logs_domain.apply_context_to_log(current_user, text, payload)
    else:
        misunderstood_domain.handle_misunderstood(current_user, string_payload)


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
    if nlp.is_help_domain(processed_text):
        help_domain.handle(current_user, text, processed_text)

    elif nlp.is_habits_domain(current_user, processed_text):
        habits_domain.handle_habits_text(current_user, text, processed_text)

    elif nlp.is_logs_domain(current_user, processed_text):
        logs_domain.handle_logs_text(current_user, text)

    elif nlp.is_todo_domain(current_user, processed_text):
        todo_domain.handle_todo(current_user, text, processed_text)

    elif nlp.is_ridesharing_domain(processed_text):
        ridesharing_domain.handle(current_user, text, processed_text)

    else:
        misunderstood_domain.handle_misunderstood(
            current_user,
            text,
            processed_text
        )
