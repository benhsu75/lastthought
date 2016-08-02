from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *
from main import messenger_helper

import random
from django.views.decorators.csrf import csrf_exempt
import json



def index(request):
    context = RequestContext(request, {
    })
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context))

def learn_more(request):
    context = RequestContext(request, {
    })
    template = loader.get_template('main/learn_more.html')
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
    messenger_helper.send_basic_text_message(fbid, intro_message)
    messenger_helper.send_basic_text_message(fbid, second_message)

def handle_message_received(fbid, text):
    try:
        current_user = User.objects.get(fbid=fbid)
    except User.DoesNotExist:
        messenger_helper.send_basic_text_message(fbid,"Something went wrong :(")
        return

    state = current_user.state
    text = text.lower()

    if(state == 0):
        create_first_goal_flow(current_user, fbid, text)
        print('STATE=0')
    elif(text == 'goals'):
        print("IN GOALS")
        messenger_helper.send_button_message(fbid, "Manage your goals:", [
                {
                    'type': 'web_url',
                    'url': 'http://userdatagraph.herokuapp.com/goals/'+fbid+'/list',
                    'title': 'See Goals'    
                },
                {
                    'type': 'web_url',
                    'url': 'http://userdatagraph.herokuapp.com/goals/'+fbid+'/add',
                    'title': 'Add Goal'    
                }
            ])
    elif(text == 'show me my goals'):
        # button_list = []
        # goal_list = Goal.objects.filter(user=current_user)
        # for g in goal_list:
        #     button_list.append({
        #             'type': 'web_url',
        #             'url': 'http://userdatagraph.herokuapp.com/goals/'+str(g.id)+'/show',
        #             'title': g.name
        #         })

        # messenger_helper.send_button_message(fbid, "Your goals:", button_list)
        messenger_helper.send_button_message(fbid, "Manage your goals:", [
                {
                    'type': 'web_url',
                    'url': 'http://userdatagraph.herokuapp.com/goals/'+fbid+'/list',
                    'title': 'See Goals'    
                },
                {
                    'type': 'web_url',
                    'url': 'http://userdatagraph.herokuapp.com/goals/'+fbid+'/add',
                    'title': 'Add Goal'    
                }
            ])
    else:
        messenger_helper.send_basic_text_message(fbid, "Sorry, I don't understand.")

def handle_postback(fbid):
    return

def create_first_goal_flow(current_user, fbid, text):
    if(current_user.state == 0):
        # Parse out name from text
        name = text
        name_tokenized = name.split(' ')
        first_name = name_tokenized[0]

        # Update user
        current_user.full_name = name
        current_user.first_name = first_name
        current_user.save()

        # Send message about how to use
        how_to_use_message = "Nice to meet you, " + first_name + "! I'm here to make it easier for you to do things. I can help you track reminders, set goals, and more."
        messenger_helper.send_basic_text_message(fbid, how_to_use_message)

        learn_more_message = "To learn more about everything I can help you with, click Learn More!"
        messenger_helper.send_button_message(fbid, learn_more_message, [
                {
                    'type': 'web_url',
                    'url': 'http://userdatagraph.herokuapp.com/learn_more',
                    'title': 'Learn More'    
                }
            ])

        # Update user state
        current_user.state = 1
        current_user.save()

    else:
        return

def delete_users(request):
    all_users = User.objects.all()
    num_of_users_deleted = len(all_users)
    for u in all_users:
        u.delete()

    return HttpResponse("Deleted " + str(num_of_users_deleted) + " users!")


