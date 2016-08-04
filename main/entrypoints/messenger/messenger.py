from django.http import HttpResponse
from main.models import *
from main.entrypoints.messenger import send_api_helper

import random
from django.views.decorators.csrf import csrf_exempt
import json


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
    send_api_helper.send_basic_text_message(fbid, intro_message)
    send_api_helper.send_basic_text_message(fbid, second_message)



BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_postback(fbid):
    return

def handle_message_received(fbid, text):
    try:
        current_user = User.objects.get(fbid=fbid)
    except User.DoesNotExist:
        send_api_helper.send_basic_text_message(fbid,"Something went wrong :(")
        return

    state = current_user.state
    text = text.lower()

    if(state == 0):
        onboard_flow(current_user, fbid, text)
        print('STATE=0')
    elif(text == 'goals'):
        # send_api_helper.send_button_message(fbid, "Your goals:", button_list)
        send_api_helper.send_button_message(fbid, "Manage your goals:", [
                {
                    'type': 'web_url',
                    'url': BASE_HEROKU_URL + '/users/'+fbid+'/goals',
                    'title': 'See Goals'    
                },
                {
                    'type': 'web_url',
                    'url': BASE_HEROKU_URL + '/users/'+fbid+'/add_goal',
                    'title': 'Add Goal'    
                }
            ])
    elif(text == 'show me my goals'):

        # send_api_helper.send_button_message(fbid, "Your goals:", button_list)
        send_api_helper.send_button_message(fbid, "Manage your goals:", [
                {
                    'type': 'web_url',
                    'url': BASE_HEROKU_URL + '/users/'+fbid+'/goals',
                    'title': 'See Goals'    
                },
                {
                    'type': 'web_url',
                    'url': BASE_HEROKU_URL + '/users/'+fbid+'/add_goal',
                    'title': 'Add Goal'    
                }
            ])
    elif(text == 'todo'):
        send_api_helper.send_button_message(fbid, "Your todo list:", [
                {
                    'type': 'web_url',
                    'url': BASE_HEROKU_URL + '/users/'+fbid+'/todo',
                    'title': 'To Do List'
                }
            ])
    elif('add todo' in text):
        # Create todo
        todo_text = text.replace('add todo', '')

        todo = ToDoTask(text=todo_text, user=current_user)
        todo.save()

        # Send message telling them that we created the todo
        send_api_helper.send_basic_text_message(fbid,'"'+todo_text+'" added to your to do list!')

    else:
        send_api_helper.send_basic_text_message(fbid, "Sorry, I don't understand.")

######################################
################## OTHER #############
######################################

def onboard_flow(current_user, fbid, text):
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
        send_api_helper.send_basic_text_message(fbid, how_to_use_message)

        learn_more_message = "To learn more about everything I can help you with, click Learn More!"
        send_api_helper.send_button_message(fbid, learn_more_message, [
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
