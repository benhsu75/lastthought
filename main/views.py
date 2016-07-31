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
    verify_token = 'userdatagraph_verify_token'

    if(request.GET['hub.verify_token'] == verify_token):
        challenge = request.GET['hub.challenge']

    print("RESPONDING")

    return HttpResponse(challenge)
