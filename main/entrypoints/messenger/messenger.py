from django.http import HttpResponse
from main.models import *
from main.entrypoints.messenger import send_api_helper

import random
from django.views.decorators.csrf import csrf_exempt
import json
from main.message_log import message_log
from main.utils import nlp
from main.domains import goals_domain, onboarding_domain, todo_domain, misunderstood_domain

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

            # Handle different webhooks times
            if 'message' in messaging:
                # Message received webhook
                print('# Message received webhook')
                message_text = messaging['message']['text']
                handle_message_received(fbid, message_text)
            elif 'optin' in messaging:
                # Plugin authentication webhook
                print('# Authentication')
                handle_optin(fbid)
            elif 'postback' in messaging:
                # Postback webhook
                print('# Postback webhook')
                handle_postback(fbid)

    return HttpResponse(status=200)

# Sends the user our initial message 
def handle_optin(fbid):
    # Check if user exists, if it does, do nothing
    try:
        current_user = User.objects.get(fbid=fbid)

        return # Do nothing
    except User.DoesNotExist:
        pass

    # If user doesn't exist, create user
    u = User(fbid=fbid, state=0)
    u.save()

    # Send user intro message
    welcome_message = "Hey! Nice to meet you. I'm Jarvis, here to help be your better self :)."
    send_api_helper.send_basic_text_message(fbid, intro_message)
    message_log.log_message('welcome_message', current_user, welcome_message, None)

    ask_for_name_message = "To begin, what's your full name?"
    send_api_helper.send_basic_text_message(fbid, second_message)
    message_log.log_message('ask_for_name_message', current_user, ask_for_name_message, None)

def handle_postback(fbid):
    return

def handle_message_received(fbid, text):
    try:
        current_user = User.objects.get(fbid=fbid)
    except User.DoesNotExist:
        send_api_helper.send_basic_text_message(fbid,"Something went wrong :(")
        return

    if(nlp.is_onboarding_domain(current_user, text)):

        onboarding_domain.handle_onboard_flow(current_user, fbid, text)
    
    elif(nlp.is_goals_domain(current_user, text)):

        goals_domain.handle_goals(current_user, text)

    elif(nlp.is_todo_domain(current_user, text)):

        todo_domain.handle_todo(current_user, text)

    else:

        misunderstood_domain.handle_misunderstood(current_user, text)
        

