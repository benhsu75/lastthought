from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import TestModel, User, Goal, GoalEntry

import random
from django.views.decorators.csrf import csrf_exempt
import json
import requests


def test(request):
    # Each time the page loads create a db object
    t = TestModel(random_number = random.randint(0,10))
    t.save()

    context = RequestContext(request, {
        'page_visits': len(TestModel.objects.all())
    })
    template = loader.get_template('main/test.html')
    return HttpResponse(template.render(context))

def index(request):
    context = RequestContext(request, {
        'page_visits': len(TestModel.objects.all())
    })
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context))

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
                handle_authentication(fbid)

            elif 'postback' in messaging:
                # Postback webhook
                print('# Postback webhook')
                handle_postback(fbid)

    return HttpResponse(status=200)

# Sends the user our initial message 
def handle_authentication(fbid):
    # Check if user exists, if it does, do nothing
    try:
        print("# USER EXISTS")
        current_user = User.objects.get(fbid=fbid)

        return # Do nothing
    except User.DoesNotExist:
        pass

    # If user doesn't exist, create user
    print("# CREATING USER")
    u = User(fbid=fbid, state=0)
    u.save()

    # Send user intro message
    intro_message = "Hey! Nice to meet you. I'm Jarvis, here to help be your better self :)."
    second_message = "To begin, what's your full name?"
    send_basic_text_message(fbid, intro_message)
    send_basic_text_message(fbid, second_message)

def handle_message_received(fbid, text):
    try:
        current_user = User.objects.get(fbid=fbid)
    except User.DoesNotExist:
        send_basic_text_message(fbid,"Something went wrong :(")
        return

    state = current_user.state
    if(state == 0):
        create_first_goal_flow(current_user, fbid, text)
    else:
        send_basic_text_message(fbid, "Sorry, I don't understand.")

def handle_postback(fbid):
    return

def create_first_goal_flow(current_user, fbid, text):
    if(current_user.state == 0):
        # Parse out name from text
        print("NAME: " + text)
    else:
        return



# Helper method to send message
PAGE_ACCESS_TOKEN = 'EAADqZAUs43F4BAM24X91sSlhAIU7UHnLyO6eNp1rGMmQncyKsz34AgvlqfJKRnn3rNfYLMZBZA914L5z9MO8G6AVsGhljVUZCZAYtNfjbt0NKX7FFHDjOPvBcsiZCNzpSdNVZC4lCsbHVevRIhzKxFzjFzAMDVWq4W8KNuqtxXt8QZDZD'
SEND_BASE_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token='

def send_basic_text_message(fbid, text):
    send_payload = {
        'recipient': {
            'id': fbid
        },
        'message': {
            'text': text
        }
    }
    url_to_post = SEND_BASE_URL + PAGE_ACCESS_TOKEN
    r = requests.post(url_to_post, json=send_payload)
    print(r.text)
    print("SENT MESSAGE")

def delete_users(request):
    all_users = User.objects.all()
    num_of_users_deleted = len(all_users)
    for u in all_users:
        u.delete()

    return HttpResponse("Deleted " + str(num_of_users_deleted) + " users!")


