from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import TestModel

import random
from django.views.decorators.csrf import csrf_exempt


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

    # Print request for debugging
    print("------RECEIVED MESSAGE (BODY BELOW)------")
    print(request.body)
    print("------DONE PRINTING------------")

    # Loop through multiple entries
    entry_list = request.body['entry']
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
            elif 'optin' in messaging:
                # Plugin authentication webhook
                print('# Authentication')
            elif 'postback' in messaging:
                # Postback webhook
                print('# Postback webhook')
            
    

    return HttpResponse(status=200)
