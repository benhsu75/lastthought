from django.http import HttpResponse
from main.models import *
from main.entrypoints.messenger import send_api_helper

import random
from django.views.decorators.csrf import csrf_exempt
import json
from main.message_log import message_log
from main.utils import nlp, helper_util
from main.domains import habits_domain, onboarding_domain, todo_domain, misunderstood_domain

######################################
######### MESSENGER WEBHOOK ##########
######################################

@csrf_exempt
def messenger_callback(request):

    # Challenge verification
    if('hub.challenge' in request.GET):
        print("REQUEST IS A CHALLENGE")
        return HttpResponse(request.GET['hub.challenge'])

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

            print("# FBID: " + fbid)

            if(not helper_util.user_exists(fbid)):
                print 'creating new user'
                onboarding_domain.create_new_user(fbid)
                continue

            # Handle different webhooks times
            if 'message' in messaging:
                print 'handling message'
                # Message received webhook
                message_text = messaging['message']['text']
                handle_message_received(fbid, message_text)
            elif 'optin' in messaging:
                print 'handling optin'
                # Plugin authentication webhook
                handle_optin(fbid)
            elif 'postback' in messaging:
                print 'handling postback'
                # Postback webhook
                payload = message['postback']['payload']
                handle_postback(fbid, payload)

    return HttpResponse(status=200)

# Sends the user our initial message 
def handle_optin(fbid):
    # Check if user exists, if it does, do nothing
    try:
        current_user = User.objects.get(fbid=fbid)

        return # Do nothing
    except User.DoesNotExist:
        pass

    onboarding_domain.create_new_user(fbid)

def handle_postback(fbid, string_payload):
    payload = json.loads(string_payload)

    state = payload['state']

    # Get current user
    if helper_util.user_exists(fbid):
        current_user = User.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)
        # Should never get here

    if state == 'habit_binary_response':
        habits_domain.handle_binary_postback(current_user, payload)
    else:
        misunderstood_domain.handle_misunderstood(current_user, string_payload)


def handle_message_received(fbid, text):
    try:
        current_user = User.objects.get(fbid=fbid)
    except User.DoesNotExist:
        send_api_helper.send_basic_text_message(fbid,"Something went wrong :(")
        return

    # Use nlp to determine which domain it goes under, then triage to that domain. The domain handles the sub-triaging within itself
    if(nlp.is_onboarding_domain(current_user, text)):

        onboarding_domain.handle_onboard_flow(current_user, fbid, text)
    
    elif(nlp.is_habits_domain(current_user, text)):

        habits_domain.handle_habits_text(current_user, text)

    elif(nlp.is_todo_domain(current_user, text)):

        todo_domain.handle_todo(current_user, text)

    else:

        misunderstood_domain.handle_misunderstood(current_user, text)
        

