from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import TestModel

import random


def test(request):
    # Each time the page loads create a db object
    t = TestModel(random_number = random.randint(0,10))
    t.save()


    context = RequestContext(request, {
        'page_visits': len(TestModel.objects.all())
    })
    template = loader.get_template('main/test.html')
    return HttpResponse(template.render(context))


def messenger_callback(request):
    print("!!!!!!!TESTING")
    verify_token = 'userdatagraph_verify_token'

    # Verify from FB
    if('hub.verify_token' not in request.GET or request.GET['hub.verify_token'] != verify_token):
        return HttpResponse("This endpoint only receives from Facebook Messenger", status=500)

    # Challenge verification
    if('hub.challenge' in request.GET):
        return HttpResponse(request.GET['hub.challenge'])

    # Print request for debugging
    print("------RECEIVED MESSAGE------")
    print(request)

    return HttpResponse(status=200)
